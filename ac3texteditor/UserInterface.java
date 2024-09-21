/*
 * Copyright (C) 2014 Dashman
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * UserInterface.java
 *
 * Created on 02-feb-2014, 22:58:37
 */

package ac3texteditor;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontFormatException;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GraphicsEnvironment;
import java.awt.Image;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.awt.image.IndexColorModel;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.GroupLayout;

/**
 *
 * @author Jonatan
 */
public class UserInterface extends javax.swing.JFrame {

    String lastDirectoryFile = ".";
    String currentFile = "";
    String lastDirectoryTextures = ".";

    PreviewPanel previewFile = new PreviewPanel();
    PreviewPanel previewEdit = new PreviewPanel();

    BufferedImage imgEdit;
    BufferedImage imgFinal;

    Font ac3font;
    boolean fontLoaded;

    IndexColorModel icm1;
    IndexColorModel icm2;
    IndexColorModel icm3;
    IndexColorModel icm4;
    IndexColorModel icm5;
    IndexColorModel icm6;
    IndexColorModel icm7;
    IndexColorModel icm8;
    IndexColorModel icm9;
    IndexColorModel icm10;
    IndexColorModel icm11;
    IndexColorModel icm12;
    IndexColorModel icm13;
    IndexColorModel icm14;
    IndexColorModel icm15;
    IndexColorModel icm16;
    IndexColorModel icm17;
    IndexColorModel icm18;
    IndexColorModel icm19;
    IndexColorModel icm20;
    IndexColorModel icm21;
    IndexColorModel icm22;
    IndexColorModel icm23;
    IndexColorModel icm24;
    IndexColorModel icm25;
    IndexColorModel icm26;
    IndexColorModel icm27;
    IndexColorModel icm28;
    IndexColorModel icm29;
    IndexColorModel icm30;

    // Colours to be used in the CLUTs

    /*
        f8 f8 e8   08 38 40
        d0 d0 c0   08 68 68
        88 88 80   08 98 90
        38 38 38   08 c8 c0
        98 90 a0
        e0 d0 a0
        90 d0 80
        e0 90 80
        48 90 98
        d8 88 b0
        d0 08 b8
        80 50 a8
        10 10 98
        48 d0 80
        e0 d0 70
        18 90 70
     */
    Color white1 = new Color(248, 248, 232);
    Color lgray1 = new Color(208, 208, 192);
    Color dgray1 = new Color(136, 136, 128);
    Color black1 = new Color(56, 56, 56);

    Color extra01 = new Color(152, 144, 160);
    Color extra02 = new Color(232, 208, 160);
    Color extra03 = new Color(144, 208, 128);
    Color extra04 = new Color(232, 144, 128);
    Color extra05 = new Color(72, 144, 152);
    Color extra06 = new Color(216, 136, 176);
    Color extra07 = new Color(208, 8, 184);
    Color extra08 = new Color(128, 80, 168);
    Color extra09 = new Color(16, 16, 152);
    Color extra10 = new Color(72, 208, 112);
    Color extra11 = new Color(232, 208, 96);
    Color extra12 = new Color(24, 144, 96);

    /*
        f8 f8 e8   08 38 40
        d0 d0 c0   08 68 68
        88 88 80   08 98 90
        38 38 38   08 c8 c0
     */

    Color blue1 = new Color(8, 56, 64);
    Color blue2 = new Color(8, 104, 104);
    Color blue3 = new Color(8, 152, 144);
    Color blue4 = new Color(8, 200, 192);

    /*
     f0 f0 f0 (240)
     c0 c0 c0 (192)
     58 58 58 (88)
     01 00 00
     */

    Color black2 = new Color(1, 0, 0);
    Color dgray2 = new Color(88, 88, 88);
    Color lgray2 = new Color(192, 192, 192);
    Color white2 = new Color(240, 240, 240);


    IndexColorModel[] CLUTs;
    int CLUT_in_use = 0;
    byte[] r;
    byte[] g;
    byte[] b;

    JComboBox<String> fontComboBox;
    JComboBox<Integer> fontSizeComboBox;
    JLabel fontSelectLabel;
    JLabel fontSizeLabel;

    /** Creates new form UserInterface */
    public UserInterface() {
        initComponents();
        URL location = getClass().getResource("/Neucom.png");
        if (location == null) {
            System.err.println("Icon not found: /Neucom.png");
        } else {
            this.setIconImage(new ImageIcon(location).getImage());
        }

        panelShow.setBounds(0, 0, scrollPreview.getWidth(), scrollPreview.getHeight());
        scrollPreview.setViewportView(panelShow);
        panelShow.add(previewFile);
        panelShow.add(previewEdit);

        prepareCLUTs();
        displayCLUT();

        imgEdit = new BufferedImage(1, 1, BufferedImage.TYPE_BYTE_BINARY, CLUTs[CLUT_in_use]);

        //System.out.print(java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment().getAllFonts());
        fontLoaded = false;

        try {
            // Register the "small" font
            InputStream is = getClass().getResourceAsStream("/custom.ttf");
            if (is != null) {
                ac3font = Font.createFont(Font.TRUETYPE_FONT, is);
                fontLoaded = true;
            } else {
                System.err.println("Font file not found in JAR root: /custom.ttf");
            }
        } catch (FontFormatException | IOException ex) {
            Logger.getLogger(UserInterface.class.getName()).log(Level.SEVERE, null, ex);
        }

        // Initialize font selection components
        initFontSelection();
    }

    private void initFontSelection() {
        // Get available fonts
        String[] fonts = GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames();
        fontComboBox = new JComboBox<>(fonts);
        fontComboBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent evt) {
                updateFont();
            }
        });

        // Font size options
        Integer[] fontSizes = {10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30};
        fontSizeComboBox = new JComboBox<>(fontSizes);
        fontSizeComboBox.setSelectedItem(12); // Default size
        fontSizeComboBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent evt) {
                updateFont();
            }
        });

        // Labels for font selection and size
        fontSelectLabel = new JLabel("Font select:");
        fontSizeLabel = new JLabel("Font size:");

        // Adjust layout
        GroupLayout layout = new GroupLayout(panelText);
        panelText.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(textareaTranslation, GroupLayout.DEFAULT_SIZE, 380, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(labelTextColor)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(comboTextColor, GroupLayout.PREFERRED_SIZE, 150, GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(fontSelectLabel)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(fontComboBox, GroupLayout.PREFERRED_SIZE, 150, GroupLayout.PREFERRED_SIZE)
                        .addGap(20)
                        .addComponent(fontSizeLabel)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(fontSizeComboBox, GroupLayout.PREFERRED_SIZE, 70, GroupLayout.PREFERRED_SIZE)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(textareaTranslation, GroupLayout.PREFERRED_SIZE, 200, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(labelTextColor)
                    .addComponent(comboTextColor, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(fontSelectLabel)
                    .addComponent(fontComboBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(fontSizeLabel)
                    .addComponent(fontSizeComboBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
    }

    private void updateFont() {
        String selectedFont = (String) fontComboBox.getSelectedItem();
        int selectedSize = (Integer) fontSizeComboBox.getSelectedItem();
        previewEdit.setFont(new Font(selectedFont, Font.PLAIN, selectedSize));
        previewEdit.repaint();
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        groupFontSize = new javax.swing.ButtonGroup();
        panelOriginal = new javax.swing.JPanel();
        labelOriginal = new javax.swing.JLabel();
        buttonOriginal = new javax.swing.JButton();
        panelText = new javax.swing.JPanel();
        scrollPaneTexto = new javax.swing.JScrollPane();
        textareaTranslation = new javax.swing.JTextArea();
        labelTextColor = new javax.swing.JLabel();
        labelBackground = new javax.swing.JLabel();
        comboBackground = new javax.swing.JComboBox();
        comboTextColor = new javax.swing.JComboBox();
        radioFontSmall = new javax.swing.JRadioButton();
        radioFontBig = new javax.swing.JRadioButton();
        checkLayers = new javax.swing.JCheckBox();
        checkSecondLayer = new javax.swing.JCheckBox();
        checkInverted = new javax.swing.JCheckBox();
        checkLineSpacing = new javax.swing.JCheckBox();
        checkFlip = new javax.swing.JCheckBox();
        panelOutput = new javax.swing.JPanel();
        labelDestination = new javax.swing.JLabel();
        labelFilename = new javax.swing.JLabel();
        textfieldDestination = new javax.swing.JTextField();
        buttonDestination = new javax.swing.JButton();
        textfieldFilename = new javax.swing.JTextField();
        buttonGenerate = new javax.swing.JButton();
        checkHalf = new javax.swing.JCheckBox();
        panelPreview = new javax.swing.JPanel();
        scrollPreview = new javax.swing.JScrollPane();
        panelShow = new javax.swing.JPanel();
        labelOriginalPreview = new javax.swing.JLabel();
        labelTranslated = new javax.swing.JLabel();
        panelCLUT = new javax.swing.JPanel();
        labelCLUT = new javax.swing.JLabel();
        panelColor1 = new javax.swing.JPanel();
        panelColor2 = new javax.swing.JPanel();
        panelColor3 = new javax.swing.JPanel();
        panelColor4 = new javax.swing.JPanel();
        panelColor5 = new javax.swing.JPanel();
        panelColor6 = new javax.swing.JPanel();
        panelColor7 = new javax.swing.JPanel();
        panelColor8 = new javax.swing.JPanel();
        panelColor9 = new javax.swing.JPanel();
        panelColor10 = new javax.swing.JPanel();
        panelColor11 = new javax.swing.JPanel();
        panelColor12 = new javax.swing.JPanel();
        panelColor13 = new javax.swing.JPanel();
        panelColor14 = new javax.swing.JPanel();
        panelColor15 = new javax.swing.JPanel();
        panelColor16 = new javax.swing.JPanel();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("Ace Combat 3 Text Editor v1.3.4a by Dashman, modified by aikika");
        setResizable(false);

        panelOriginal.setBorder(javax.swing.BorderFactory.createTitledBorder("Original File"));

        labelOriginal.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        labelOriginal.setText("< No file loaded >");

        buttonOriginal.setText("Browse");
        buttonOriginal.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonOriginalActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout panelOriginalLayout = new javax.swing.GroupLayout(panelOriginal);
        panelOriginal.setLayout(panelOriginalLayout);
        panelOriginalLayout.setHorizontalGroup(
            panelOriginalLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, panelOriginalLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(labelOriginal, javax.swing.GroupLayout.DEFAULT_SIZE, 320, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(buttonOriginal, javax.swing.GroupLayout.PREFERRED_SIZE, 93, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );
        panelOriginalLayout.setVerticalGroup(
            panelOriginalLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelOriginalLayout.createSequentialGroup()
                .addGroup(panelOriginalLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelOriginal)
                    .addComponent(buttonOriginal))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        panelText.setBorder(javax.swing.BorderFactory.createTitledBorder("Translated Text"));

        textareaTranslation.setColumns(20);
        textareaTranslation.setRows(5);
        textareaTranslation.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent evt) {
                textareaTranslationKeyTyped(evt);
            }
        });
        scrollPaneTexto.setViewportView(textareaTranslation);

        labelTextColor.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelTextColor.setHorizontalAlignment(javax.swing.SwingConstants.RIGHT);
        labelTextColor.setText("Text color:");

        labelBackground.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelBackground.setText("Background:");

        comboBackground.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Transparent", "Black", "White", "Blue" }));
        comboBackground.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                comboBackgroundActionPerformed(evt);
            }
        });

        comboTextColor.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Gray", "White", "Black", "Blue-ish Black" }));
        comboTextColor.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                comboTextColorActionPerformed(evt);
            }
        });

        groupFontSize.add(radioFontSmall);
        radioFontSmall.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        radioFontSmall.setSelected(true);
        radioFontSmall.setText("Small Font");
        radioFontSmall.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                radioFontSmallActionPerformed(evt);
            }
        });

        groupFontSize.add(radioFontBig);
        radioFontBig.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        radioFontBig.setText("Big Font");
        radioFontBig.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                radioFontBigActionPerformed(evt);
            }
        });

        checkLayers.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        checkLayers.setText("Layered Texture");
        checkLayers.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkLayersActionPerformed(evt);
            }
        });

        checkSecondLayer.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        checkSecondLayer.setText("Using 2nd layer");
        checkSecondLayer.setEnabled(false);
        checkSecondLayer.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkSecondLayerActionPerformed(evt);
            }
        });

        checkInverted.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        checkInverted.setText("Invert colours");
        checkInverted.setEnabled(false);
        checkInverted.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkInvertedActionPerformed(evt);
            }
        });

        checkLineSpacing.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        checkLineSpacing.setSelected(true);
        checkLineSpacing.setText("Line Spacing");
        checkLineSpacing.setEnabled(false);
        checkLineSpacing.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkLineSpacingActionPerformed(evt);
            }
        });

        checkFlip.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        checkFlip.setText("Flip 1 & 2");
        checkFlip.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkFlipActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout panelTextLayout = new javax.swing.GroupLayout(panelText);
        panelText.setLayout(panelTextLayout);
        panelTextLayout.setHorizontalGroup(
            panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(scrollPaneTexto, javax.swing.GroupLayout.DEFAULT_SIZE, 443, Short.MAX_VALUE)
            .addGroup(panelTextLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(panelTextLayout.createSequentialGroup()
                        .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                            .addComponent(labelTextColor, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(labelBackground, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addComponent(comboTextColor, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(comboBackground, 0, 138, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addGroup(panelTextLayout.createSequentialGroup()
                                .addComponent(radioFontSmall)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(radioFontBig))
                            .addComponent(checkLineSpacing, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                    .addGroup(panelTextLayout.createSequentialGroup()
                        .addComponent(checkLayers, javax.swing.GroupLayout.PREFERRED_SIZE, 120, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(checkSecondLayer)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(checkInverted)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(checkFlip)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        panelTextLayout.setVerticalGroup(
            panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelTextLayout.createSequentialGroup()
                .addComponent(scrollPaneTexto, javax.swing.GroupLayout.PREFERRED_SIZE, 142, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(checkLayers)
                    .addComponent(checkSecondLayer)
                    .addComponent(checkInverted)
                    .addComponent(checkFlip))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelBackground)
                    .addComponent(comboBackground, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(checkLineSpacing))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(panelTextLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelTextColor)
                    .addComponent(comboTextColor, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(radioFontSmall)
                    .addComponent(radioFontBig))
                .addContainerGap())
        );

        panelOutput.setBorder(javax.swing.BorderFactory.createTitledBorder("Generated File"));

        labelDestination.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelDestination.setText("Destination folder:");

        labelFilename.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelFilename.setHorizontalAlignment(javax.swing.SwingConstants.RIGHT);
        labelFilename.setText("File name:");

        textfieldDestination.setEditable(false);

        buttonDestination.setText("Browse");
        buttonDestination.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonDestinationActionPerformed(evt);
            }
        });

        textfieldFilename.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent evt) {
                textfieldFilenameKeyTyped(evt);
            }
        });

        buttonGenerate.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        buttonGenerate.setText("GENERATE");
        buttonGenerate.setActionCommand("buttonGenerate");
        buttonGenerate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonGenerateActionPerformed(evt);
            }
        });

        checkHalf.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        checkHalf.setText("Half-height");
        checkHalf.setEnabled(false);
        checkHalf.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkHalfActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout panelOutputLayout = new javax.swing.GroupLayout(panelOutput);
        panelOutput.setLayout(panelOutputLayout);
        panelOutputLayout.setHorizontalGroup(
            panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, panelOutputLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(checkHalf)
                    .addGroup(panelOutputLayout.createSequentialGroup()
                        .addGroup(panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                            .addComponent(labelFilename, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(labelDestination, javax.swing.GroupLayout.Alignment.LEADING))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addComponent(textfieldFilename, javax.swing.GroupLayout.PREFERRED_SIZE, 202, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(textfieldDestination, javax.swing.GroupLayout.PREFERRED_SIZE, 202, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(buttonGenerate, javax.swing.GroupLayout.DEFAULT_SIZE, 103, Short.MAX_VALUE)
                            .addComponent(buttonDestination, javax.swing.GroupLayout.DEFAULT_SIZE, 103, Short.MAX_VALUE))))
                .addContainerGap())
        );
        panelOutputLayout.setVerticalGroup(
            panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelOutputLayout.createSequentialGroup()
                .addGroup(panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelDestination)
                    .addComponent(textfieldDestination, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(buttonDestination))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(panelOutputLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelFilename)
                    .addComponent(textfieldFilename, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(buttonGenerate))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(checkHalf))
        );

        panelPreview.setBorder(javax.swing.BorderFactory.createTitledBorder("Preview"));
        panelPreview.setPreferredSize(new java.awt.Dimension(545, 451));

        scrollPreview.setBorder(null);

        panelShow.setPreferredSize(new java.awt.Dimension(530, 350));

        labelOriginalPreview.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelOriginalPreview.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        labelOriginalPreview.setText("ORIGINAL");
        labelOriginalPreview.setPreferredSize(new java.awt.Dimension(256, 14));

        labelTranslated.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelTranslated.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        labelTranslated.setText("TRANSLATED");
        labelTranslated.setPreferredSize(new java.awt.Dimension(256, 14));

        javax.swing.GroupLayout panelShowLayout = new javax.swing.GroupLayout(panelShow);
        panelShow.setLayout(panelShowLayout);
        panelShowLayout.setHorizontalGroup(
            panelShowLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelShowLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(labelOriginalPreview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(labelTranslated, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(23, Short.MAX_VALUE))
        );
        panelShowLayout.setVerticalGroup(
            panelShowLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelShowLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(panelShowLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(labelOriginalPreview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(labelTranslated, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(342, Short.MAX_VALUE))
        );

        scrollPreview.setViewportView(panelShow);

        panelCLUT.setBorder(javax.swing.BorderFactory.createEtchedBorder());

        labelCLUT.setFont(new java.awt.Font("Tahoma", 1, 11)); // NOI18N
        labelCLUT.setText("CLUT:");

        panelColor1.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor1Layout = new javax.swing.GroupLayout(panelColor1);
        panelColor1.setLayout(panelColor1Layout);
        panelColor1Layout.setHorizontalGroup(
            panelColor1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor1Layout.setVerticalGroup(
            panelColor1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor2.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor2Layout = new javax.swing.GroupLayout(panelColor2);
        panelColor2.setLayout(panelColor2Layout);
        panelColor2Layout.setHorizontalGroup(
            panelColor2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor2Layout.setVerticalGroup(
            panelColor2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor3.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor3Layout = new javax.swing.GroupLayout(panelColor3);
        panelColor3.setLayout(panelColor3Layout);
        panelColor3Layout.setHorizontalGroup(
            panelColor3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor3Layout.setVerticalGroup(
            panelColor3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor4.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor4Layout = new javax.swing.GroupLayout(panelColor4);
        panelColor4.setLayout(panelColor4Layout);
        panelColor4Layout.setHorizontalGroup(
            panelColor4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor4Layout.setVerticalGroup(
            panelColor4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor5.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor5Layout = new javax.swing.GroupLayout(panelColor5);
        panelColor5.setLayout(panelColor5Layout);
        panelColor5Layout.setHorizontalGroup(
            panelColor5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor5Layout.setVerticalGroup(
            panelColor5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor6.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor6Layout = new javax.swing.GroupLayout(panelColor6);
        panelColor6.setLayout(panelColor6Layout);
        panelColor6Layout.setHorizontalGroup(
            panelColor6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor6Layout.setVerticalGroup(
            panelColor6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor7.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor7Layout = new javax.swing.GroupLayout(panelColor7);
        panelColor7.setLayout(panelColor7Layout);
        panelColor7Layout.setHorizontalGroup(
            panelColor7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor7Layout.setVerticalGroup(
            panelColor7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor8.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor8Layout = new javax.swing.GroupLayout(panelColor8);
        panelColor8.setLayout(panelColor8Layout);
        panelColor8Layout.setHorizontalGroup(
            panelColor8Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor8Layout.setVerticalGroup(
            panelColor8Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor9.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor9Layout = new javax.swing.GroupLayout(panelColor9);
        panelColor9.setLayout(panelColor9Layout);
        panelColor9Layout.setHorizontalGroup(
            panelColor9Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor9Layout.setVerticalGroup(
            panelColor9Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor10.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor10Layout = new javax.swing.GroupLayout(panelColor10);
        panelColor10.setLayout(panelColor10Layout);
        panelColor10Layout.setHorizontalGroup(
            panelColor10Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor10Layout.setVerticalGroup(
            panelColor10Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor11.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor11Layout = new javax.swing.GroupLayout(panelColor11);
        panelColor11.setLayout(panelColor11Layout);
        panelColor11Layout.setHorizontalGroup(
            panelColor11Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor11Layout.setVerticalGroup(
            panelColor11Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor12.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor12Layout = new javax.swing.GroupLayout(panelColor12);
        panelColor12.setLayout(panelColor12Layout);
        panelColor12Layout.setHorizontalGroup(
            panelColor12Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor12Layout.setVerticalGroup(
            panelColor12Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor13.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor13Layout = new javax.swing.GroupLayout(panelColor13);
        panelColor13.setLayout(panelColor13Layout);
        panelColor13Layout.setHorizontalGroup(
            panelColor13Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor13Layout.setVerticalGroup(
            panelColor13Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor14.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor14Layout = new javax.swing.GroupLayout(panelColor14);
        panelColor14.setLayout(panelColor14Layout);
        panelColor14Layout.setHorizontalGroup(
            panelColor14Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor14Layout.setVerticalGroup(
            panelColor14Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor15.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor15Layout = new javax.swing.GroupLayout(panelColor15);
        panelColor15.setLayout(panelColor15Layout);
        panelColor15Layout.setHorizontalGroup(
            panelColor15Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor15Layout.setVerticalGroup(
            panelColor15Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        panelColor16.setPreferredSize(new java.awt.Dimension(25, 25));

        javax.swing.GroupLayout panelColor16Layout = new javax.swing.GroupLayout(panelColor16);
        panelColor16.setLayout(panelColor16Layout);
        panelColor16Layout.setHorizontalGroup(
            panelColor16Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );
        panelColor16Layout.setVerticalGroup(
            panelColor16Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 25, Short.MAX_VALUE)
        );

        javax.swing.GroupLayout panelCLUTLayout = new javax.swing.GroupLayout(panelCLUT);
        panelCLUT.setLayout(panelCLUTLayout);
        panelCLUTLayout.setHorizontalGroup(
            panelCLUTLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelCLUTLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(labelCLUT)
                .addGap(18, 18, 18)
                .addComponent(panelColor1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor5, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor6, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor7, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor8, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor9, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor10, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor11, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor12, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor13, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor14, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor15, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelColor16, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(14, Short.MAX_VALUE))
        );
        panelCLUTLayout.setVerticalGroup(
            panelCLUTLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelCLUTLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(panelCLUTLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(labelCLUT)
                    .addGroup(panelCLUTLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addComponent(panelColor1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor5, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor6, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor7, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor8, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor9, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor10, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor11, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor12, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor13, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor14, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor15, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(panelColor16, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(14, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout panelPreviewLayout = new javax.swing.GroupLayout(panelPreview);
        panelPreview.setLayout(panelPreviewLayout);
        panelPreviewLayout.setHorizontalGroup(
            panelPreviewLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(panelCLUT, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addComponent(scrollPreview, javax.swing.GroupLayout.DEFAULT_SIZE, 563, Short.MAX_VALUE)
        );
        panelPreviewLayout.setVerticalGroup(
            panelPreviewLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelPreviewLayout.createSequentialGroup()
                .addComponent(panelCLUT, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(scrollPreview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(21, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                    .addComponent(panelOutput, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(panelOriginal, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(panelText, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(panelPreview, javax.swing.GroupLayout.PREFERRED_SIZE, 579, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                    .addComponent(panelPreview, javax.swing.GroupLayout.Alignment.LEADING, 0, 454, Short.MAX_VALUE)
                    .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                        .addComponent(panelOriginal, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(panelText, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(panelOutput, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void buttonDestinationActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonDestinationActionPerformed
        // TODO add your handling code here:
        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new java.io.File(lastDirectoryTextures));
        chooser.setDialogTitle("Select directory to generate textures");
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

        // disable the "All files" option.
        chooser.setAcceptAllFileFilterUsed(false);

        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION){
            //System.out.println("getCurrentDirectory(): " +  chooser.getCurrentDirectory());
            //System.out.println("getSelectedFile() : " +  chooser.getSelectedFile());
            lastDirectoryTextures = chooser.getSelectedFile().getAbsolutePath();
            textfieldDestination.setText(lastDirectoryTextures);
        }
    }//GEN-LAST:event_buttonDestinationActionPerformed

    private void buttonOriginalActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonOriginalActionPerformed
        // TODO add your handling code here:
        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new java.io.File(lastDirectoryFile));
        chooser.setDialogTitle("Select original texture");
        chooser.setFileSelectionMode(JFileChooser.OPEN_DIALOG);

        // disable the "All files" option.
        chooser.setAcceptAllFileFilterUsed(false);
        chooser.setFileFilter(new FileNameExtensionFilter("Image file", "bmp"));

        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION){
            //System.out.println("getCurrentDirectory(): " +  chooser.getCurrentDirectory());
            //System.out.println("getSelectedFile() : " +  chooser.getSelectedFile());
            lastDirectoryFile = chooser.getSelectedFile().getAbsolutePath();
            currentFile = chooser.getSelectedFile().getName();
            if (checkHalf.isEnabled() && checkHalf.isSelected())
                textfieldFilename.setText(currentFile.substring(0, currentFile.length() - 4) + "-half.bmp");
            else
                textfieldFilename.setText(currentFile);
            labelOriginal.setText(currentFile);

            showPreview();
        }
    }//GEN-LAST:event_buttonOriginalActionPerformed

    private void textareaTranslationKeyTyped(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_textareaTranslationKeyTyped
        // TODO add your handling code here:
        String txt = textareaTranslation.getText();

        boolean isBackspace = evt.getKeyChar() == '\u0008'; // BACKSPACE
        boolean isDelete = evt.getKeyChar() == ''; // DELETE (copied from the output. it works)
        if (!isBackspace && !isDelete){  // Add the new character
            int position = textareaTranslation.getCaretPosition();
            txt = txt.substring(0, position) + evt.getKeyChar() + txt.substring(position);
        }

        writeEdit(txt);
}//GEN-LAST:event_comboBackgroundActionPerformed

    private void buttonGenerateActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonGenerateActionPerformed
        // TODO add your handling code here:
        if(textfieldFilename.getText().trim().isEmpty()){
            JOptionPane.showMessageDialog(null, "Please write a filename!",
                    "Error", JOptionPane.ERROR_MESSAGE);
        }
        else{   // Save the texture
            if (checkHalf.isEnabled() && checkHalf.isSelected())
                saveHalfTexture();
            else{
                //imgFinal = imgEdit.getSubimage(0, 0, imgEdit.getWidth(), imgEdit.getHeight());
                imgFinal = imgEdit;
                saveEditTexture();
            }
        }
    }//GEN-LAST:event_buttonGenerateActionPerformed

    private void textfieldFilenameKeyTyped(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_textfieldFilenameKeyTyped
        // TODO add your handling code here:
        if(evt.getKeyChar() == '?' || evt.getKeyChar() == '*' || evt.getKeyChar() == '"' || evt.getKeyChar() == '<'
                || evt.getKeyChar() == '>' || evt.getKeyChar() == '|' || evt.getKeyChar() == ':'  || evt.getKeyChar() == '/'
                || evt.getKeyChar() == '\\' )
            evt.consume();
    }//GEN-LAST:event_textfieldFilenameKeyTyped

    private void radioFontSmallActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_radioFontSmallActionPerformed
        // TODO add your handling code here:
        checkHalf.setEnabled(false);
        checkLineSpacing.setEnabled(false);
        if (checkHalf.isSelected()){
            String txt = textfieldFilename.getText();
            if (txt.endsWith("-half.png")){
                    textfieldFilename.setText(txt.substring(0, txt.length() - 9) + ".png");
            }
            else{
                if(txt.endsWith("-half")){
                    textfieldFilename.setText(txt.substring(0, txt.length() - 5) + "-half.png");
                }
            }
        }
        if (!textareaTranslation.getText().isEmpty())
            writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_radioFontSmallActionPerformed

    private void radioFontBigActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_radioFontBigActionPerformed
        // TODO add your handling code here:
        checkHalf.setEnabled(true);
        checkLineSpacing.setEnabled(true);
        if (checkHalf.isSelected()){
            String txt = textfieldFilename.getText();
            if(!txt.endsWith("-half.png")){
                if(txt.endsWith(".png")){
                    textfieldFilename.setText(txt.substring(0, txt.length() - 4) + "-half.png");
                }
                else{
                    if(!txt.endsWith("-half")){
                        txt = txt + "-half.png";
                        textfieldFilename.setText(txt);
                    }
                }
            }
        }
        if (!textareaTranslation.getText().isEmpty())
            writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_radioFontBigActionPerformed

    private void checkHalfActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkHalfActionPerformed
        // TODO add your handling code here:
        String txt = textfieldFilename.getText();
        if (!txt.isEmpty()){
            if (checkHalf.isSelected()){
                if(!txt.endsWith("-half.bmp")){
                    if(txt.endsWith(".bmp")){
                        textfieldFilename.setText(txt.substring(0, txt.length() - 4) + "-half.bmp");
                    }
                    else{
                        if(!txt.endsWith("-half")){
                            txt = txt + "-half.bmp";
                            textfieldFilename.setText(txt);
                        }
                    }
                }
            }
            else{
                if (txt.endsWith("-half.bmp")){
                        textfieldFilename.setText(txt.substring(0, txt.length() - 9) + ".bmp");
                }
                else{
                    if(txt.endsWith("-half")){
                        textfieldFilename.setText(txt.substring(0, txt.length() - 5) + "-half.bmp");
                    }
                }
            }
        }
    }//GEN-LAST:event_checkHalfActionPerformed

    private void checkLayersActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkLayersActionPerformed
        // TODO add your handling code here:
        boolean selected = checkLayers.isSelected();

        checkSecondLayer.setEnabled(selected);
        checkInverted.setEnabled(selected);

        labelBackground.setEnabled(!selected);
        comboBackground.setEnabled(!selected);
        labelTextColor.setEnabled(!selected);
        comboTextColor.setEnabled(!selected);

        if (selected){
            switch(CLUT_in_use){
                case 0: // BLACK background, WHITE characters
                    comboBackground.setSelectedIndex(1);
                    comboTextColor.setSelectedIndex(1);
                    break;
                case 1: // BLUE background, BLACK characters
                    comboBackground.setSelectedIndex(3);
                    comboTextColor.setSelectedIndex(3);
                    break;
                case 2: // WHITE background, BLACK characters
                    comboBackground.setSelectedIndex(2);
                    comboTextColor.setSelectedIndex(2);
                    break;
            }

            CLUT_in_use += 3;

            if (checkSecondLayer.isSelected())
                CLUT_in_use += 3;
            if (checkInverted.isSelected())
                CLUT_in_use += 6;
        }
        else{
            CLUT_in_use -= 3;

            if (checkSecondLayer.isSelected())
                CLUT_in_use -= 3;
            if (checkInverted.isSelected())
                CLUT_in_use -= 6;
        }

        //System.out.println("CLUT: " + CLUT_in_use);
        displayCLUT();

        writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_checkLayersActionPerformed

    private void checkSecondLayerActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkSecondLayerActionPerformed
        // TODO add your handling code here:
        if (checkSecondLayer.isSelected())
            CLUT_in_use += 3;
        else
            CLUT_in_use -= 3;
        
        //System.out.println("CLUT: " + CLUT_in_use);
        displayCLUT();

        writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_checkSecondLayerActionPerformed

    private void checkInvertedActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkInvertedActionPerformed
        // TODO add your handling code here:
        if (checkInverted.isSelected())
            CLUT_in_use += 6;
        else
            CLUT_in_use -= 6;

        //System.out.println("CLUT: " + CLUT_in_use);
        displayCLUT();

        writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_checkInvertedActionPerformed

    private void checkLineSpacingActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkLineSpacingActionPerformed
        // TODO add your handling code here:
        writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_checkLineSpacingActionPerformed

    private void checkFlipActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkFlipActionPerformed
        // TODO add your handling code here:
        if (checkFlip.isSelected())
            CLUT_in_use += 15;
        else
            CLUT_in_use -= 15;

        //System.out.println("CLUT: " + CLUT_in_use);
        displayCLUT();

        writeEdit(textareaTranslation.getText());
    }//GEN-LAST:event_checkFlipActionPerformed

    public void prepareCLUTs(){
        // Create our CLUTs (Color LookUp Tables)
        r = new byte[16];
        g = new byte[16];
        b = new byte[16];
        
    /*
        f8 f8 e8   08 38 40
        d0 d0 c0   08 68 68
        88 88 80   08 98 90
        38 38 38   08 c8 c0
        98 90 a0
        e0 d0 a0
        90 d0 80
        e0 90 80
        48 90 98
        d8 88 b0
        d0 08 b8
        80 50 a8
        10 10 98
        48 d0 80
        e0 d0 70
        18 90 70
     */
        r[0] = (byte) 0xf8 ; g[0] = (byte) 0xf8 ; b[0] = (byte) 0xe8 ;
        r[1] = (byte) 0xd0 ; g[1] = (byte) 0xd0 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0x88 ; g[2] = (byte) 0x88 ; b[2] = (byte) 0x80 ;
        r[3] = (byte) 0x38 ; g[3] = (byte) 0x38 ; b[3] = (byte) 0x38 ;
        r[4] = (byte) 0x98 ; g[4] = (byte) 0x90 ; b[4] = (byte) 0xa0 ;
        r[5] = (byte) 0xe0 ; g[5] = (byte) 0xd0 ; b[5] = (byte) 0xa0 ;
        r[6] = (byte) 0x90 ; g[6] = (byte) 0xd0 ; b[6] = (byte) 0x80 ;
        r[7] = (byte) 0xe0 ; g[7] = (byte) 0x90 ; b[7] = (byte) 0x80 ;
        r[8] = (byte) 0x48 ; g[8] = (byte) 0x90 ; b[8] = (byte) 0x98 ;
        r[9] = (byte) 0xd8 ; g[9] = (byte) 0x88 ; b[9] = (byte) 0xb0 ;
        r[10] = (byte) 0xd0 ; g[10] = (byte) 0x08 ; b[10] = (byte) 0xb8 ;
        r[11] = (byte) 0x80 ; g[11] = (byte) 0x50 ; b[11] = (byte) 0xa8 ;
        r[12] = (byte) 0x10 ; g[12] = (byte) 0x10 ; b[12] = (byte) 0x98 ;
        r[13] = (byte) 0x48 ; g[13] = (byte) 0xd0 ; b[13] = (byte) 0x80 ;
        r[14] = (byte) 0xe0 ; g[14] = (byte) 0xd0 ; b[14] = (byte) 0x70 ;
        r[15] = (byte) 0x18 ; g[15] = (byte) 0x0 ; b[15] = (byte) 0x70 ;

        icm1 = new IndexColorModel(4, 16, r, g, b);

        r[0] = (byte) 0xd0 ; g[0] = (byte) 0xd0 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0xf8 ; g[1] = (byte) 0xf8 ; b[1] = (byte) 0xe8 ;

        icm16 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

    /*
        f8 f8 e8   08 38 40
        d0 d0 c0   08 68 68
        88 88 80   08 98 90
        38 38 38   08 c8 c0
     */
        r[0] = (byte) 0x08 ; g[0] = (byte) 0x38 ; b[0] = (byte) 0x40 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x68 ; b[1] = (byte) 0x68 ;
        r[2] = (byte) 0x08 ; g[2] = (byte) 0x98 ; b[2] = (byte) 0x90 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0xc8 ; b[3] = (byte) 0xc0 ;

        icm2 = new IndexColorModel(4, 16, r, g, b);

        r[0] = (byte) 0x08 ; g[0] = (byte) 0x68 ; b[0] = (byte) 0x68 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x38 ; b[1] = (byte) 0x40 ;

        icm17 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

    /*
     f0 f0 f0 (240)
     c0 c0 c0 (192)
     58 58 58 (88)
     01 00 00
     */
        r[0] = (byte) 0xf0 ; g[0] = (byte) 0xf0 ; b[0] = (byte) 0xf0 ;
        r[1] = (byte) 0xc0 ; g[1] = (byte) 0xc0 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0x58 ; g[2] = (byte) 0x58 ; b[2] = (byte) 0x58 ;
        r[3] = (byte) 0x01 ; g[3] = (byte) 0x00 ; b[3] = (byte) 0x00 ;
 

        icm3 = new IndexColorModel(4, 16, r, g, b);
        
        r[0] = (byte) 0xc0 ; g[0] = (byte) 0xc0 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0xf0 ; g[1] = (byte) 0xf0 ; b[1] = (byte) 0xf0 ;

        icm18 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        // ------------------------------ FIRST LAYER ----------------------

        r[0] = (byte) 0xf0 ; g[0] = (byte) 0xf0 ; b[0] = (byte) 0xf0 ;
        r[1] = (byte) 0xc0 ; g[1] = (byte) 0xc0 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0x58 ; g[2] = (byte) 0x58 ; b[2] = (byte) 0x58 ;
        r[3] = (byte) 0x01 ; g[3] = (byte) 0x00 ; b[3] = (byte) 0x00 ;
        r[4] = (byte) 0xf0 ; g[4] = (byte) 0xf0 ; b[4] = (byte) 0xf0 ;
        r[5] = (byte) 0xc0 ; g[5] = (byte) 0xc0 ; b[5] = (byte) 0xc0 ;
        r[6] = (byte) 0x58 ; g[6] = (byte) 0x58 ; b[6] = (byte) 0x58 ;
        r[7] = (byte) 0x01 ; g[7] = (byte) 0x00 ; b[7] = (byte) 0x00 ;
        r[8] = (byte) 0xf0 ; g[8] = (byte) 0xf0 ; b[8] = (byte) 0xf0 ;
        r[9] = (byte) 0xc0 ; g[9] = (byte) 0xc0 ; b[9] = (byte) 0xc0 ;
        r[10] = (byte) 0x58 ; g[10] = (byte) 0x58 ; b[10] = (byte) 0x58 ;
        r[11] = (byte) 0x01 ; g[11] = (byte) 0x00 ; b[11] = (byte) 0x00 ;
        r[12] = (byte) 0xf0 ; g[12] = (byte) 0xf0 ; b[12] = (byte) 0xf0 ;
        r[13] = (byte) 0xc0 ; g[13] = (byte) 0xc0 ; b[13] = (byte) 0xc0 ;
        r[14] = (byte) 0x58 ; g[14] = (byte) 0x58 ; b[14] = (byte) 0x58 ;
        r[15] = (byte) 0x01 ; g[15] = (byte) 0x00 ; b[15] = (byte) 0x00 ;

        icm4 = new IndexColorModel(4, 16, r, g, b);
        
        r[0] = (byte) 0xc0 ; g[0] = (byte) 0xc0 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0xf0 ; g[1] = (byte) 0xf0 ; b[1] = (byte) 0xf0 ;
        r[4] = (byte) 0xc0 ; g[4] = (byte) 0xc0 ; b[4] = (byte) 0xc0 ;
        r[5] = (byte) 0xf0 ; g[5] = (byte) 0xf0 ; b[5] = (byte) 0xf0 ;
        r[8] = (byte) 0xc0 ; g[8] = (byte) 0xc0 ; b[8] = (byte) 0xc0 ;
        r[9] = (byte) 0xf0 ; g[9] = (byte) 0xf0 ; b[9] = (byte) 0xf0 ;
        r[12] = (byte) 0xc0 ; g[12] = (byte) 0xc0 ; b[12] = (byte) 0xc0 ;
        r[13] = (byte) 0xf0 ; g[13] = (byte) 0xf0 ; b[13] = (byte) 0xf0 ;

        icm19 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0x08 ; g[0] = (byte) 0x38 ; b[0] = (byte) 0x40 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x68 ; b[1] = (byte) 0x68 ;
        r[2] = (byte) 0x08 ; g[2] = (byte) 0x98 ; b[2] = (byte) 0x90 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0xc8 ; b[3] = (byte) 0xc0 ;
        r[4] = (byte) 0x08 ; g[4] = (byte) 0x38 ; b[4] = (byte) 0x40 ;
        r[5] = (byte) 0x08 ; g[5] = (byte) 0x68 ; b[5] = (byte) 0x68 ;
        r[6] = (byte) 0x08 ; g[6] = (byte) 0x98 ; b[6] = (byte) 0x90 ;
        r[7] = (byte) 0x08 ; g[7] = (byte) 0xc8 ; b[7] = (byte) 0xc0 ;
        r[8] = (byte) 0x08 ; g[8] = (byte) 0x38 ; b[8] = (byte) 0x40 ;
        r[9] = (byte) 0x08 ; g[9] = (byte) 0x68 ; b[9] = (byte) 0x68 ;
        r[10] = (byte) 0x08 ; g[10] = (byte) 0x98 ; b[10] = (byte) 0x90 ;
        r[11] = (byte) 0x08 ; g[11] = (byte) 0xc8 ; b[11] = (byte) 0xc0 ;
        r[12] = (byte) 0x08 ; g[12] = (byte) 0x38 ; b[12] = (byte) 0x40 ;
        r[13] = (byte) 0x08 ; g[13] = (byte) 0x68 ; b[13] = (byte) 0x68 ;
        r[14] = (byte) 0x08 ; g[14] = (byte) 0x98 ; b[14] = (byte) 0x90 ;
        r[15] = (byte) 0x08 ; g[15] = (byte) 0xc8 ; b[15] = (byte) 0xc0 ;

        icm5 = new IndexColorModel(4, 16, r, g, b);
        
        r[0] = (byte) 0x08 ; g[0] = (byte) 0x68 ; b[0] = (byte) 0x68 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x38 ; b[1] = (byte) 0x40 ;
        r[4] = (byte) 0x08 ; g[4] = (byte) 0x68 ; b[4] = (byte) 0x68 ;
        r[5] = (byte) 0x08 ; g[5] = (byte) 0x38 ; b[5] = (byte) 0x40 ;
        r[8] = (byte) 0x08 ; g[8] = (byte) 0x68 ; b[8] = (byte) 0x68 ;
        r[9] = (byte) 0x08 ; g[9] = (byte) 0x38 ; b[9] = (byte) 0x40 ;
        r[12] = (byte) 0x08 ; g[12] = (byte) 0x68 ; b[12] = (byte) 0x68 ;
        r[13] = (byte) 0x08 ; g[13] = (byte) 0x38 ; b[13] = (byte) 0x40 ;

        icm20 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0xf8 ; g[0] = (byte) 0xf8 ; b[0] = (byte) 0xe8 ;
        r[1] = (byte) 0xd0 ; g[1] = (byte) 0xd0 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0x88 ; g[2] = (byte) 0x88 ; b[2] = (byte) 0x80 ;
        r[3] = (byte) 0x38 ; g[3] = (byte) 0x38 ; b[3] = (byte) 0x38 ;
        r[4] = (byte) 0xf8 ; g[4] = (byte) 0xf8 ; b[4] = (byte) 0xe8 ;
        r[5] = (byte) 0xd0 ; g[5] = (byte) 0xd0 ; b[5] = (byte) 0xc0 ;
        r[6] = (byte) 0x88 ; g[6] = (byte) 0x88 ; b[6] = (byte) 0x80 ;
        r[7] = (byte) 0x38 ; g[7] = (byte) 0x38 ; b[7] = (byte) 0x38 ;
        r[8] = (byte) 0xf8 ; g[8] = (byte) 0xf8 ; b[8] = (byte) 0xe8 ;
        r[9] = (byte) 0xd0 ; g[9] = (byte) 0xd0 ; b[9] = (byte) 0xc0 ;
        r[10] = (byte) 0x88 ; g[10] = (byte) 0x88 ; b[10] = (byte) 0x80 ;
        r[11] = (byte) 0x38 ; g[11] = (byte) 0x38 ; b[11] = (byte) 0x38 ;
        r[12] = (byte) 0xf8 ; g[12] = (byte) 0xf8 ; b[12] = (byte) 0xe8 ;
        r[13] = (byte) 0xd0 ; g[13] = (byte) 0xd0 ; b[13] = (byte) 0xc0 ;
        r[14] = (byte) 0x88 ; g[14] = (byte) 0x88 ; b[14] = (byte) 0x80 ;
        r[15] = (byte) 0x38 ; g[15] = (byte) 0x38 ; b[15] = (byte) 0x38 ;
        
        icm6 = new IndexColorModel(4, 16, r, g, b);
        
        r[0] = (byte) 0xd0 ; g[0] = (byte) 0xd0 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0xf8 ; g[1] = (byte) 0xf8 ; b[1] = (byte) 0xe8 ;
        r[4] = (byte) 0xd0 ; g[4] = (byte) 0xd0 ; b[4] = (byte) 0xc0 ;
        r[5] = (byte) 0xf8 ; g[5] = (byte) 0xf8 ; b[5] = (byte) 0xe8 ;
        r[8] = (byte) 0xd0 ; g[8] = (byte) 0xd0 ; b[8] = (byte) 0xc0 ;
        r[9] = (byte) 0xf8 ; g[9] = (byte) 0xf8 ; b[9] = (byte) 0xe8 ;
        r[12] = (byte) 0xd0 ; g[12] = (byte) 0xd0 ; b[12] = (byte) 0xc0 ;
        r[13] = (byte) 0xf8 ; g[13] = (byte) 0xf8 ; b[13] = (byte) 0xe8 ;

        icm21 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        // ------------------------------ SECOND LAYER ----------------------

        r[0] = (byte) 0xf0 ; g[0] = (byte) 0xf0 ; b[0] = (byte) 0xf0 ;
        r[1] = (byte) 0xf0 ; g[1] = (byte) 0xf0 ; b[1] = (byte) 0xf0 ;
        r[2] = (byte) 0xf0 ; g[2] = (byte) 0xf0 ; b[2] = (byte) 0xf0 ;
        r[3] = (byte) 0xf0 ; g[3] = (byte) 0xf0 ; b[3] = (byte) 0xf0 ;
        r[4] = (byte) 0xc0 ; g[4] = (byte) 0xc0 ; b[4] = (byte) 0xc0 ;
        r[5] = (byte) 0xc0 ; g[5] = (byte) 0xc0 ; b[5] = (byte) 0xc0 ;
        r[6] = (byte) 0xc0 ; g[6] = (byte) 0xc0 ; b[6] = (byte) 0xc0 ;
        r[7] = (byte) 0xc0 ; g[7] = (byte) 0xc0 ; b[7] = (byte) 0xc0 ;
        r[8] = (byte) 0x58 ; g[8] = (byte) 0x58 ; b[8] = (byte) 0x58 ;
        r[9] = (byte) 0x58 ; g[9] = (byte) 0x58 ; b[9] = (byte) 0x58 ;
        r[10] = (byte) 0x58 ; g[10] = (byte) 0x58 ; b[10] = (byte) 0x58 ;
        r[11] = (byte) 0x58 ; g[11] = (byte) 0x58 ; b[11] = (byte) 0x58 ;
        r[12] = (byte) 0x01 ; g[12] = (byte) 0x00 ; b[12] = (byte) 0x00 ;
        r[13] = (byte) 0x01 ; g[13] = (byte) 0x00 ; b[13] = (byte) 0x00 ;
        r[14] = (byte) 0x01 ; g[14] = (byte) 0x00 ; b[14] = (byte) 0x00 ;
        r[15] = (byte) 0x01 ; g[15] = (byte) 0x00 ; b[15] = (byte) 0x00 ;

        icm7 = new IndexColorModel(4, 16, r, g, b);

        r[0] = (byte) 0xc0 ; g[0] = (byte) 0xc0 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0xc0 ; g[1] = (byte) 0xc0 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0xc0 ; g[2] = (byte) 0xc0 ; b[2] = (byte) 0xc0 ;
        r[3] = (byte) 0xc0 ; g[3] = (byte) 0xc0 ; b[3] = (byte) 0xc0 ;
        r[4] = (byte) 0xf0 ; g[4] = (byte) 0xf0 ; b[4] = (byte) 0xf0 ;
        r[5] = (byte) 0xf0 ; g[5] = (byte) 0xf0 ; b[5] = (byte) 0xf0 ;
        r[6] = (byte) 0xf0 ; g[6] = (byte) 0xf0 ; b[6] = (byte) 0xf0 ;
        r[7] = (byte) 0xf0 ; g[7] = (byte) 0xf0 ; b[7] = (byte) 0xf0 ;

        icm22 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0x08 ; g[0] = (byte) 0x38 ; b[0] = (byte) 0x40 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x38 ; b[1] = (byte) 0x40 ;
        r[2] = (byte) 0x08 ; g[2] = (byte) 0x38 ; b[2] = (byte) 0x40 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0x38 ; b[3] = (byte) 0x40 ;
        r[4] = (byte) 0x08 ; g[4] = (byte) 0x68 ; b[4] = (byte) 0x68 ;
        r[5] = (byte) 0x08 ; g[5] = (byte) 0x68 ; b[5] = (byte) 0x68 ;
        r[6] = (byte) 0x08 ; g[6] = (byte) 0x68 ; b[6] = (byte) 0x68 ;
        r[7] = (byte) 0x08 ; g[7] = (byte) 0x68 ; b[7] = (byte) 0x68 ;
        r[8] = (byte) 0x08 ; g[8] = (byte) 0x98 ; b[8] = (byte) 0x90 ;
        r[9] = (byte) 0x08 ; g[9] = (byte) 0x98 ; b[9] = (byte) 0x90 ;
        r[10] = (byte) 0x08 ; g[10] = (byte) 0x98 ; b[10] = (byte) 0x90 ;
        r[11] = (byte) 0x08 ; g[11] = (byte) 0x98 ; b[11] = (byte) 0x90 ;
        r[12] = (byte) 0x08 ; g[12] = (byte) 0xc8 ; b[12] = (byte) 0xc0 ;
        r[13] = (byte) 0x08 ; g[13] = (byte) 0xc8 ; b[13] = (byte) 0xc0 ;
        r[14] = (byte) 0x08 ; g[14] = (byte) 0xc8 ; b[14] = (byte) 0xc0 ;
        r[15] = (byte) 0x08 ; g[15] = (byte) 0xc8 ; b[15] = (byte) 0xc0 ;

        icm8 = new IndexColorModel(4, 16, r, g, b);

        r[0] = (byte) 0x08 ; g[0] = (byte) 0x68 ; b[0] = (byte) 0x68 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x68 ; b[1] = (byte) 0x68 ;
        r[2] = (byte) 0x08 ; g[2] = (byte) 0x68 ; b[2] = (byte) 0x68 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0x68 ; b[3] = (byte) 0x68 ;
        r[4] = (byte) 0x08 ; g[4] = (byte) 0x38 ; b[4] = (byte) 0x40 ;
        r[5] = (byte) 0x08 ; g[5] = (byte) 0x38 ; b[5] = (byte) 0x40 ;
        r[6] = (byte) 0x08 ; g[6] = (byte) 0x38 ; b[6] = (byte) 0x40 ;
        r[7] = (byte) 0x08 ; g[7] = (byte) 0x38 ; b[7] = (byte) 0x40 ;

        icm23 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0xf8 ; g[0] = (byte) 0xf8 ; b[0] = (byte) 0xe8 ;
        r[1] = (byte) 0xf8 ; g[1] = (byte) 0xf8 ; b[1] = (byte) 0xe8 ;
        r[2] = (byte) 0xf8 ; g[2] = (byte) 0xf8 ; b[2] = (byte) 0xe8 ;
        r[3] = (byte) 0xf8 ; g[3] = (byte) 0xf8 ; b[3] = (byte) 0xe8 ;
        r[4] = (byte) 0xd0 ; g[4] = (byte) 0xd0 ; b[4] = (byte) 0xc0 ;
        r[5] = (byte) 0xd0 ; g[5] = (byte) 0xd0 ; b[5] = (byte) 0xc0 ;
        r[6] = (byte) 0xd0 ; g[6] = (byte) 0xd0 ; b[6] = (byte) 0xc0 ;
        r[7] = (byte) 0xd0 ; g[7] = (byte) 0xd0 ; b[7] = (byte) 0xc0 ;
        r[8] = (byte) 0x88 ; g[8] = (byte) 0x88 ; b[8] = (byte) 0x80 ;
        r[9] = (byte) 0x88 ; g[9] = (byte) 0x88 ; b[9] = (byte) 0x80 ;
        r[10] = (byte) 0x88 ; g[10] = (byte) 0x88 ; b[10] = (byte) 0x80 ;
        r[11] = (byte) 0x88 ; g[11] = (byte) 0x88 ; b[11] = (byte) 0x80 ;
        r[12] = (byte) 0x38 ; g[12] = (byte) 0x38 ; b[12] = (byte) 0x38 ;
        r[13] = (byte) 0x38 ; g[13] = (byte) 0x38 ; b[13] = (byte) 0x38 ;
        r[14] = (byte) 0x38 ; g[14] = (byte) 0x38 ; b[14] = (byte) 0x38 ;
        r[15] = (byte) 0x38 ; g[15] = (byte) 0x38 ; b[15] = (byte) 0x38 ;

        icm9 = new IndexColorModel(4, 16, r, g, b);

        r[0] = (byte) 0xd0 ; g[0] = (byte) 0xd0 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0xd0 ; g[1] = (byte) 0xd0 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0xd0 ; g[2] = (byte) 0xd0 ; b[2] = (byte) 0xc0 ;
        r[3] = (byte) 0xd0 ; g[3] = (byte) 0xd0 ; b[3] = (byte) 0xc0 ;
        r[4] = (byte) 0xf8 ; g[4] = (byte) 0xf8 ; b[4] = (byte) 0xe8 ;
        r[5] = (byte) 0xf8 ; g[5] = (byte) 0xf8 ; b[5] = (byte) 0xe8 ;
        r[6] = (byte) 0xf8 ; g[6] = (byte) 0xf8 ; b[6] = (byte) 0xe8 ;
        r[7] = (byte) 0xf8 ; g[7] = (byte) 0xf8 ; b[7] = (byte) 0xe8 ;

        icm24 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        // -------------------------- FIRST LAYER INVERSED ------------------

        r[0] = (byte) 0x01 ; g[0] = (byte) 0x00 ; b[0] = (byte) 0x00 ;
        r[1] = (byte) 0x58 ; g[1] = (byte) 0x58 ; b[1] = (byte) 0x58 ;
        r[2] = (byte) 0xc0 ; g[2] = (byte) 0xc0 ; b[2] = (byte) 0xc0 ;
        r[3] = (byte) 0xf0 ; g[3] = (byte) 0xf0 ; b[3] = (byte) 0xf0 ;
        r[4] = (byte) 0x01 ; g[4] = (byte) 0x00 ; b[4] = (byte) 0x00 ;
        r[5] = (byte) 0x58 ; g[5] = (byte) 0x58 ; b[5] = (byte) 0x58 ;
        r[6] = (byte) 0xc0 ; g[6] = (byte) 0xc0 ; b[6] = (byte) 0xc0 ;
        r[7] = (byte) 0xf0 ; g[7] = (byte) 0xf0 ; b[7] = (byte) 0xf0 ;
        r[8] = (byte) 0x01 ; g[8] = (byte) 0x00 ; b[8] = (byte) 0x00 ;
        r[9] = (byte) 0x58 ; g[9] = (byte) 0x58 ; b[9] = (byte) 0x58 ;
        r[10] = (byte) 0xc0 ; g[10] = (byte) 0xc0 ; b[10] = (byte) 0xc0 ;
        r[11] = (byte) 0xf0 ; g[11] = (byte) 0xf0 ; b[11] = (byte) 0xf0 ;
        r[12] = (byte) 0x01 ; g[12] = (byte) 0x00 ; b[12] = (byte) 0x00 ;
        r[13] = (byte) 0x58 ; g[13] = (byte) 0x58 ; b[13] = (byte) 0x58 ;
        r[14] = (byte) 0xc0 ; g[14] = (byte) 0xc0 ; b[14] = (byte) 0xc0 ;
        r[15] = (byte) 0xf0 ; g[15] = (byte) 0xf0 ; b[15] = (byte) 0xf0 ;

        icm10 = new IndexColorModel(4, 16, r, g, b);
        
        r[2] = (byte) 0xf0 ; g[2] = (byte) 0xf0 ; b[2] = (byte) 0xf0 ;
        r[3] = (byte) 0xc0 ; g[3] = (byte) 0xc0 ; b[3] = (byte) 0xc0 ;
        r[6] = (byte) 0xf0 ; g[6] = (byte) 0xf0 ; b[6] = (byte) 0xf0 ;
        r[7] = (byte) 0xc0 ; g[7] = (byte) 0xc0 ; b[7] = (byte) 0xc0 ;
        r[10] = (byte) 0xf0 ; g[10] = (byte) 0xf0 ; b[10] = (byte) 0xf0 ;
        r[11] = (byte) 0xc0 ; g[11] = (byte) 0xc0 ; b[11] = (byte) 0xc0 ;
        r[14] = (byte) 0xf0 ; g[14] = (byte) 0xf0 ; b[14] = (byte) 0xf0 ;
        r[15] = (byte) 0xc0 ; g[15] = (byte) 0xc0 ; b[15] = (byte) 0xc0 ;

        icm25 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0x08 ; g[0] = (byte) 0xc8 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0x98 ; b[1] = (byte) 0x90 ;
        r[2] = (byte) 0x08 ; g[2] = (byte) 0x68 ; b[2] = (byte) 0x68 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0x38 ; b[3] = (byte) 0x40 ;
        r[4] = (byte) 0x08 ; g[4] = (byte) 0xc8 ; b[4] = (byte) 0xc0 ;
        r[5] = (byte) 0x08 ; g[5] = (byte) 0x98 ; b[5] = (byte) 0x90 ;
        r[6] = (byte) 0x08 ; g[6] = (byte) 0x68 ; b[6] = (byte) 0x68 ;
        r[7] = (byte) 0x08 ; g[7] = (byte) 0x38 ; b[7] = (byte) 0x40 ;
        r[8] = (byte) 0x08 ; g[8] = (byte) 0xc8 ; b[8] = (byte) 0xc0 ;
        r[9] = (byte) 0x08 ; g[9] = (byte) 0x98 ; b[9] = (byte) 0x90 ;
        r[10] = (byte) 0x08 ; g[10] = (byte) 0x68 ; b[10] = (byte) 0x68 ;
        r[11] = (byte) 0x08 ; g[11] = (byte) 0x38 ; b[11] = (byte) 0x40 ;
        r[12] = (byte) 0x08 ; g[12] = (byte) 0xc8 ; b[12] = (byte) 0xc0 ;
        r[13] = (byte) 0x08 ; g[13] = (byte) 0x98 ; b[13] = (byte) 0x90 ;
        r[14] = (byte) 0x08 ; g[14] = (byte) 0x68 ; b[14] = (byte) 0x68 ;
        r[15] = (byte) 0x08 ; g[15] = (byte) 0x38 ; b[15] = (byte) 0x40 ;
        
        icm11 = new IndexColorModel(4, 16, r, g, b);
        
        r[2] = (byte) 0x08 ; g[2] = (byte) 0x38 ; b[2] = (byte) 0x40 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0x68 ; b[3] = (byte) 0x68 ;
        r[6] = (byte) 0x08 ; g[6] = (byte) 0x38 ; b[6] = (byte) 0x40 ;
        r[7] = (byte) 0x08 ; g[7] = (byte) 0x68 ; b[7] = (byte) 0x68 ;
        r[10] = (byte) 0x08 ; g[10] = (byte) 0x38 ; b[10] = (byte) 0x40 ;
        r[11] = (byte) 0x08 ; g[11] = (byte) 0x68 ; b[11] = (byte) 0x68 ;
        r[14] = (byte) 0x08 ; g[14] = (byte) 0x38 ; b[14] = (byte) 0x40 ;
        r[15] = (byte) 0x08 ; g[15] = (byte) 0x68 ; b[15] = (byte) 0x68 ;

        icm26 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0x38 ; g[0] = (byte) 0x38 ; b[0] = (byte) 0x38 ;
        r[1] = (byte) 0x88 ; g[1] = (byte) 0x88 ; b[1] = (byte) 0x80 ;
        r[2] = (byte) 0xd0 ; g[2] = (byte) 0xd0 ; b[2] = (byte) 0xc0 ;
        r[3] = (byte) 0xf8 ; g[3] = (byte) 0xf8 ; b[3] = (byte) 0xe8 ;
        r[4] = (byte) 0x38 ; g[4] = (byte) 0x38 ; b[4] = (byte) 0x38 ;
        r[5] = (byte) 0x88 ; g[5] = (byte) 0x88 ; b[5] = (byte) 0x80 ;
        r[6] = (byte) 0xd0 ; g[6] = (byte) 0xd0 ; b[6] = (byte) 0xc0 ;
        r[7] = (byte) 0xf8 ; g[7] = (byte) 0xf8 ; b[7] = (byte) 0xe8 ;
        r[8] = (byte) 0x38 ; g[8] = (byte) 0x38 ; b[8] = (byte) 0x38 ;
        r[9] = (byte) 0x88 ; g[9] = (byte) 0x88 ; b[9] = (byte) 0x80 ;
        r[10] = (byte) 0xd0 ; g[10] = (byte) 0xd0 ; b[10] = (byte) 0xc0 ;
        r[11] = (byte) 0xf8 ; g[11] = (byte) 0xf8 ; b[11] = (byte) 0xe8 ;
        r[12] = (byte) 0x38 ; g[12] = (byte) 0x38 ; b[12] = (byte) 0x38 ;
        r[13] = (byte) 0x88 ; g[13] = (byte) 0x88 ; b[13] = (byte) 0x80 ;
        r[14] = (byte) 0xd0 ; g[14] = (byte) 0xd0 ; b[14] = (byte) 0xc0 ;
        r[15] = (byte) 0xf8 ; g[15] = (byte) 0xf8 ; b[15] = (byte) 0xe8 ;

        icm12 = new IndexColorModel(4, 16, r, g, b);
        
        r[2] = (byte) 0xf8 ; g[2] = (byte) 0xf8 ; b[2] = (byte) 0xe8 ;
        r[3] = (byte) 0xd0 ; g[3] = (byte) 0xd0 ; b[3] = (byte) 0xc0 ;
        r[6] = (byte) 0xf8 ; g[6] = (byte) 0xf8 ; b[6] = (byte) 0xe8 ;
        r[7] = (byte) 0xd0 ; g[7] = (byte) 0xd0 ; b[7] = (byte) 0xc0 ;
        r[10] = (byte) 0xf8 ; g[10] = (byte) 0xf8 ; b[10] = (byte) 0xe8 ;
        r[11] = (byte) 0xd0 ; g[11] = (byte) 0xd0 ; b[11] = (byte) 0xc0 ;
        r[14] = (byte) 0xf8 ; g[14] = (byte) 0xf8 ; b[14] = (byte) 0xe8 ;
        r[15] = (byte) 0xd0 ; g[15] = (byte) 0xd0 ; b[15] = (byte) 0xc0 ;

        icm27 = new IndexColorModel(4, 16, r, g, b);    // Flipped version


        // -------------------------- SECOND LAYER INVERSED ------------------

        r[0] = (byte) 0x01 ; g[0] = (byte) 0x00 ; b[0] = (byte) 0x00 ;
        r[1] = (byte) 0x01 ; g[1] = (byte) 0x00 ; b[1] = (byte) 0x00 ;
        r[2] = (byte) 0x01 ; g[2] = (byte) 0x00 ; b[2] = (byte) 0x00 ;
        r[3] = (byte) 0x01 ; g[3] = (byte) 0x00 ; b[3] = (byte) 0x00 ;
        r[4] = (byte) 0x58 ; g[4] = (byte) 0x58 ; b[4] = (byte) 0x58 ;
        r[5] = (byte) 0x58 ; g[5] = (byte) 0x58 ; b[5] = (byte) 0x58 ;
        r[6] = (byte) 0x58 ; g[6] = (byte) 0x58 ; b[6] = (byte) 0x58 ;
        r[7] = (byte) 0x58 ; g[7] = (byte) 0x58 ; b[7] = (byte) 0x58 ;
        r[8] = (byte) 0xc0 ; g[8] = (byte) 0xc0 ; b[8] = (byte) 0xc0 ;
        r[9] = (byte) 0xc0 ; g[9] = (byte) 0xc0 ; b[9] = (byte) 0xc0 ;
        r[10] = (byte) 0xc0 ; g[10] = (byte) 0xc0 ; b[10] = (byte) 0xc0 ;
        r[11] = (byte) 0xc0 ; g[11] = (byte) 0xc0 ; b[11] = (byte) 0xc0 ;
        r[12] = (byte) 0xf0 ; g[12] = (byte) 0xf0 ; b[12] = (byte) 0xf0 ;
        r[13] = (byte) 0xf0 ; g[13] = (byte) 0xf0 ; b[13] = (byte) 0xf0 ;
        r[14] = (byte) 0xf0 ; g[14] = (byte) 0xf0 ; b[14] = (byte) 0xf0 ;
        r[15] = (byte) 0xf0 ; g[15] = (byte) 0xf0 ; b[15] = (byte) 0xf0 ;

        icm13 = new IndexColorModel(4, 16, r, g, b);
        
        r[8] = (byte) 0xf0 ; g[8] = (byte) 0xf0 ; b[8] = (byte) 0xf0 ;
        r[9] = (byte) 0xf0 ; g[9] = (byte) 0xf0 ; b[9] = (byte) 0xf0 ;
        r[10] = (byte) 0xf0 ; g[10] = (byte) 0xf0 ; b[10] = (byte) 0xf0 ;
        r[11] = (byte) 0xf0 ; g[11] = (byte) 0xf0 ; b[11] = (byte) 0xf0 ;
        r[12] = (byte) 0xc0 ; g[12] = (byte) 0xc0 ; b[12] = (byte) 0xc0 ;
        r[13] = (byte) 0xc0 ; g[13] = (byte) 0xc0 ; b[13] = (byte) 0xc0 ;
        r[14] = (byte) 0xc0 ; g[14] = (byte) 0xc0 ; b[14] = (byte) 0xc0 ;
        r[15] = (byte) 0xc0 ; g[15] = (byte) 0xc0 ; b[15] = (byte) 0xc0 ;

        icm28 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0x08 ; g[0] = (byte) 0xc8 ; b[0] = (byte) 0xc0 ;
        r[1] = (byte) 0x08 ; g[1] = (byte) 0xc8 ; b[1] = (byte) 0xc0 ;
        r[2] = (byte) 0x08 ; g[2] = (byte) 0xc8 ; b[2] = (byte) 0xc0 ;
        r[3] = (byte) 0x08 ; g[3] = (byte) 0xc8 ; b[3] = (byte) 0xc0 ;
        r[4] = (byte) 0x08 ; g[4] = (byte) 0x98 ; b[4] = (byte) 0x90 ;
        r[5] = (byte) 0x08 ; g[5] = (byte) 0x98 ; b[5] = (byte) 0x90 ;
        r[6] = (byte) 0x08 ; g[6] = (byte) 0x98 ; b[6] = (byte) 0x90 ;
        r[7] = (byte) 0x08 ; g[7] = (byte) 0x98 ; b[7] = (byte) 0x90 ;
        r[8] = (byte) 0x08 ; g[8] = (byte) 0x68 ; b[8] = (byte) 0x68 ;
        r[9] = (byte) 0x08 ; g[9] = (byte) 0x68 ; b[9] = (byte) 0x68 ;
        r[10] = (byte) 0x08 ; g[10] = (byte) 0x68 ; b[10] = (byte) 0x68 ;
        r[11] = (byte) 0x08 ; g[11] = (byte) 0x68 ; b[11] = (byte) 0x68 ;
        r[12] = (byte) 0x08 ; g[12] = (byte) 0x38 ; b[12] = (byte) 0x40 ;
        r[13] = (byte) 0x08 ; g[13] = (byte) 0x38 ; b[13] = (byte) 0x40 ;
        r[14] = (byte) 0x08 ; g[14] = (byte) 0x38 ; b[14] = (byte) 0x40 ;
        r[15] = (byte) 0x08 ; g[15] = (byte) 0x38 ; b[15] = (byte) 0x40 ;

        icm14 = new IndexColorModel(4, 16, r, g, b);
        
        r[8] = (byte) 0x08 ; g[8] = (byte) 0x38 ; b[8] = (byte) 0x40 ;
        r[9] = (byte) 0x08 ; g[9] = (byte) 0x38 ; b[9] = (byte) 0x40 ;
        r[10] = (byte) 0x08 ; g[10] = (byte) 0x38 ; b[10] = (byte) 0x40 ;
        r[11] = (byte) 0x08 ; g[11] = (byte) 0x38 ; b[11] = (byte) 0x40 ;
        r[12] = (byte) 0x08 ; g[12] = (byte) 0x68 ; b[12] = (byte) 0x68 ;
        r[13] = (byte) 0x08 ; g[13] = (byte) 0x68 ; b[13] = (byte) 0x68 ;
        r[14] = (byte) 0x08 ; g[14] = (byte) 0x68 ; b[14] = (byte) 0x68 ;
        r[15] = (byte) 0x08 ; g[15] = (byte) 0x68 ; b[15] = (byte) 0x68 ;

        icm29 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        r[0] = (byte) 0x38 ; g[0] = (byte) 0x38 ; b[0] = (byte) 0x38 ;
        r[1] = (byte) 0x38 ; g[1] = (byte) 0x38 ; b[1] = (byte) 0x38 ;
        r[2] = (byte) 0x38 ; g[2] = (byte) 0x38 ; b[2] = (byte) 0x38 ;
        r[3] = (byte) 0x38 ; g[3] = (byte) 0x38 ; b[3] = (byte) 0x38 ;
        r[4] = (byte) 0x88 ; g[4] = (byte) 0x88 ; b[4] = (byte) 0x80 ;
        r[5] = (byte) 0x88 ; g[5] = (byte) 0x88 ; b[5] = (byte) 0x80 ;
        r[6] = (byte) 0x88 ; g[6] = (byte) 0x88 ; b[6] = (byte) 0x80 ;
        r[7] = (byte) 0x88 ; g[7] = (byte) 0x88 ; b[7] = (byte) 0x80 ;
        r[8] = (byte) 0xd0 ; g[8] = (byte) 0xd0 ; b[8] = (byte) 0xc0 ;
        r[9] = (byte) 0xd0 ; g[9] = (byte) 0xd0 ; b[9] = (byte) 0xc0 ;
        r[10] = (byte) 0xd0 ; g[10] = (byte) 0xd0 ; b[10] = (byte) 0xc0 ;
        r[11] = (byte) 0xd0 ; g[11] = (byte) 0xd0 ; b[11] = (byte) 0xc0 ;
        r[12] = (byte) 0xf8 ; g[12] = (byte) 0xf8 ; b[12] = (byte) 0xe8 ;
        r[13] = (byte) 0xf8 ; g[13] = (byte) 0xf8 ; b[13] = (byte) 0xe8 ;
        r[14] = (byte) 0xf8 ; g[14] = (byte) 0xf8 ; b[14] = (byte) 0xe8 ;
        r[15] = (byte) 0xf8 ; g[15] = (byte) 0xf8 ; b[15] = (byte) 0xe8 ;

        icm15 = new IndexColorModel(4, 16, r, g, b);
        
        r[8] = (byte) 0xf8 ; g[8] = (byte) 0xf8 ; b[8] = (byte) 0xe8 ;
        r[9] = (byte) 0xf8 ; g[9] = (byte) 0xf8 ; b[9] = (byte) 0xe8 ;
        r[10] = (byte) 0xf8 ; g[10] = (byte) 0xf8 ; b[10] = (byte) 0xe8 ;
        r[11] = (byte) 0xf8 ; g[11] = (byte) 0xf8 ; b[11] = (byte) 0xe8 ;
        r[12] = (byte) 0xd0 ; g[12] = (byte) 0xd0 ; b[12] = (byte) 0xc0 ;
        r[13] = (byte) 0xd0 ; g[13] = (byte) 0xd0 ; b[13] = (byte) 0xc0 ;
        r[14] = (byte) 0xd0 ; g[14] = (byte) 0xd0 ; b[14] = (byte) 0xc0 ;
        r[15] = (byte) 0xd0 ; g[15] = (byte) 0xd0 ; b[15] = (byte) 0xc0 ;

        icm30 = new IndexColorModel(4, 16, r, g, b);    // Flipped version

        CLUTs = new IndexColorModel[30];
        CLUTs[0] = icm3;
        CLUTs[1] = icm2;
        CLUTs[2] = icm1;
        CLUTs[3] = icm4;
        CLUTs[4] = icm5;
        CLUTs[5] = icm6;
        CLUTs[6] = icm7;
        CLUTs[7] = icm8;
        CLUTs[8] = icm9;
        CLUTs[9] = icm10;
        CLUTs[10] = icm11;
        CLUTs[11] = icm12;
        CLUTs[12] = icm13;
        CLUTs[13] = icm14;
        CLUTs[14] = icm15;

        CLUTs[15] = icm16;
        CLUTs[16] = icm17;
        CLUTs[17] = icm18;
        CLUTs[18] = icm19;
        CLUTs[19] = icm20;
        CLUTs[20] = icm21;
        CLUTs[21] = icm22;
        CLUTs[22] = icm23;
        CLUTs[23] = icm24;
        CLUTs[24] = icm25;
        CLUTs[25] = icm26;
        CLUTs[26] = icm27;
        CLUTs[27] = icm28;
        CLUTs[28] = icm29;
        CLUTs[29] = icm30;
    }

    public void displayCLUT(){
        switch(CLUT_in_use){
            case 0:
                panelColor1.setBackground(white2);
                panelColor2.setBackground(lgray2);
                panelColor3.setBackground(dgray2);
                panelColor4.setBackground(black2);
                panelColor5.setBackground(extra01);
                panelColor6.setBackground(extra02);
                panelColor7.setBackground(extra03);
                panelColor8.setBackground(extra04);
                panelColor9.setBackground(extra05);
                panelColor10.setBackground(extra06);
                panelColor11.setBackground(extra07);
                panelColor12.setBackground(extra08);
                panelColor13.setBackground(extra09);
                panelColor14.setBackground(extra10);
                panelColor15.setBackground(extra11);
                panelColor16.setBackground(extra12);
                break;
            case 1:
                panelColor1.setBackground(blue1);
                panelColor2.setBackground(blue2);
                panelColor3.setBackground(blue3);
                panelColor4.setBackground(blue4);
                panelColor5.setBackground(extra01);
                panelColor6.setBackground(extra02);
                panelColor7.setBackground(extra03);
                panelColor8.setBackground(extra04);
                panelColor9.setBackground(extra05);
                panelColor10.setBackground(extra06);
                panelColor11.setBackground(extra07);
                panelColor12.setBackground(extra08);
                panelColor13.setBackground(extra09);
                panelColor14.setBackground(extra10);
                panelColor15.setBackground(extra11);
                panelColor16.setBackground(extra12);
                break;
            case 2:
                panelColor1.setBackground(white1);
                panelColor2.setBackground(lgray1);
                panelColor3.setBackground(dgray1);
                panelColor4.setBackground(black1);
                panelColor5.setBackground(extra01);
                panelColor6.setBackground(extra02);
                panelColor7.setBackground(extra03);
                panelColor8.setBackground(extra04);
                panelColor9.setBackground(extra05);
                panelColor10.setBackground(extra06);
                panelColor11.setBackground(extra07);
                panelColor12.setBackground(extra08);
                panelColor13.setBackground(extra09);
                panelColor14.setBackground(extra10);
                panelColor15.setBackground(extra11);
                panelColor16.setBackground(extra12);
                break;

                // FIRST LAYER
            case 3:
                panelColor1.setBackground(white2);
                panelColor2.setBackground(lgray2);
                panelColor3.setBackground(dgray2);
                panelColor4.setBackground(black2);
                panelColor5.setBackground(white2);
                panelColor6.setBackground(lgray2);
                panelColor7.setBackground(dgray2);
                panelColor8.setBackground(black2);
                panelColor9.setBackground(white2);
                panelColor10.setBackground(lgray2);
                panelColor11.setBackground(dgray2);
                panelColor12.setBackground(black2);
                panelColor13.setBackground(white2);
                panelColor14.setBackground(lgray2);
                panelColor15.setBackground(dgray2);
                panelColor16.setBackground(black2);
                break;
            case 4:
                panelColor1.setBackground(blue1);
                panelColor2.setBackground(blue2);
                panelColor3.setBackground(blue3);
                panelColor4.setBackground(blue4);
                panelColor5.setBackground(blue1);
                panelColor6.setBackground(blue2);
                panelColor7.setBackground(blue3);
                panelColor8.setBackground(blue4);
                panelColor9.setBackground(blue1);
                panelColor10.setBackground(blue2);
                panelColor11.setBackground(blue3);
                panelColor12.setBackground(blue4);
                panelColor13.setBackground(blue1);
                panelColor14.setBackground(blue2);
                panelColor15.setBackground(blue3);
                panelColor16.setBackground(blue4);
                break;
            case 5:
                panelColor1.setBackground(white1);
                panelColor2.setBackground(lgray1);
                panelColor3.setBackground(dgray1);
                panelColor4.setBackground(black1);
                panelColor5.setBackground(white1);
                panelColor6.setBackground(lgray1);
                panelColor7.setBackground(dgray1);
                panelColor8.setBackground(black1);
                panelColor9.setBackground(white1);
                panelColor10.setBackground(lgray1);
                panelColor11.setBackground(dgray1);
                panelColor12.setBackground(black1);
                panelColor13.setBackground(white1);
                panelColor14.setBackground(lgray1);
                panelColor15.setBackground(dgray1);
                panelColor16.setBackground(black1);
                break;

                // SECOND LAYER
            case 6:
                panelColor1.setBackground(white2);
                panelColor2.setBackground(white2);
                panelColor3.setBackground(white2);
                panelColor4.setBackground(white2);
                panelColor5.setBackground(lgray2);
                panelColor6.setBackground(lgray2);
                panelColor7.setBackground(lgray2);
                panelColor8.setBackground(lgray2);
                panelColor9.setBackground(dgray2);
                panelColor10.setBackground(dgray2);
                panelColor11.setBackground(dgray2);
                panelColor12.setBackground(dgray2);
                panelColor13.setBackground(black2);
                panelColor14.setBackground(black2);
                panelColor15.setBackground(black2);
                panelColor16.setBackground(black2);
                break;
            case 7:
                panelColor1.setBackground(blue1);
                panelColor2.setBackground(blue1);
                panelColor3.setBackground(blue1);
                panelColor4.setBackground(blue1);
                panelColor5.setBackground(blue2);
                panelColor6.setBackground(blue2);
                panelColor7.setBackground(blue2);
                panelColor8.setBackground(blue2);
                panelColor9.setBackground(blue3);
                panelColor10.setBackground(blue3);
                panelColor11.setBackground(blue3);
                panelColor12.setBackground(blue3);
                panelColor13.setBackground(blue4);
                panelColor14.setBackground(blue4);
                panelColor15.setBackground(blue4);
                panelColor16.setBackground(blue4);
                break;
            case 8:
                panelColor1.setBackground(white1);
                panelColor2.setBackground(white1);
                panelColor3.setBackground(white1);
                panelColor4.setBackground(white1);
                panelColor5.setBackground(lgray1);
                panelColor6.setBackground(lgray1);
                panelColor7.setBackground(lgray1);
                panelColor8.setBackground(lgray1);
                panelColor9.setBackground(dgray1);
                panelColor10.setBackground(dgray1);
                panelColor11.setBackground(dgray1);
                panelColor12.setBackground(dgray1);
                panelColor13.setBackground(black1);
                panelColor14.setBackground(black1);
                panelColor15.setBackground(black1);
                panelColor16.setBackground(black1);
                break;

                // FIRST LAYER INVERTED
            case 9:
                panelColor1.setBackground(black2);
                panelColor2.setBackground(dgray2);
                panelColor3.setBackground(lgray2);
                panelColor4.setBackground(white2);
                panelColor5.setBackground(black2);
                panelColor6.setBackground(dgray2);
                panelColor7.setBackground(lgray2);
                panelColor8.setBackground(white2);
                panelColor9.setBackground(black2);
                panelColor10.setBackground(dgray2);
                panelColor11.setBackground(lgray2);
                panelColor12.setBackground(white2);
                panelColor13.setBackground(black2);
                panelColor14.setBackground(dgray2);
                panelColor15.setBackground(lgray2);
                panelColor16.setBackground(white2);
                break;
            case 10:
                panelColor1.setBackground(blue4);
                panelColor2.setBackground(blue3);
                panelColor3.setBackground(blue2);
                panelColor4.setBackground(blue1);
                panelColor5.setBackground(blue4);
                panelColor6.setBackground(blue3);
                panelColor7.setBackground(blue2);
                panelColor8.setBackground(blue1);
                panelColor9.setBackground(blue4);
                panelColor10.setBackground(blue3);
                panelColor11.setBackground(blue2);
                panelColor12.setBackground(blue1);
                panelColor13.setBackground(blue4);
                panelColor14.setBackground(blue3);
                panelColor15.setBackground(blue2);
                panelColor16.setBackground(blue1);
                break;
            case 11:
                panelColor1.setBackground(black1);
                panelColor2.setBackground(dgray1);
                panelColor3.setBackground(lgray1);
                panelColor4.setBackground(white1);
                panelColor5.setBackground(black1);
                panelColor6.setBackground(dgray1);
                panelColor7.setBackground(lgray1);
                panelColor8.setBackground(white1);
                panelColor9.setBackground(black1);
                panelColor10.setBackground(dgray1);
                panelColor11.setBackground(lgray1);
                panelColor12.setBackground(white1);
                panelColor13.setBackground(black1);
                panelColor14.setBackground(dgray1);
                panelColor15.setBackground(lgray1);
                panelColor16.setBackground(white1);
                break;

                // SECOND LAYER INVERTED
            case 12:
                panelColor1.setBackground(black2);
                panelColor2.setBackground(black2);
                panelColor3.setBackground(black2);
                panelColor4.setBackground(black2);
                panelColor5.setBackground(dgray2);
                panelColor6.setBackground(dgray2);
                panelColor7.setBackground(dgray2);
                panelColor8.setBackground(dgray2);
                panelColor9.setBackground(lgray2);
                panelColor10.setBackground(lgray2);
                panelColor11.setBackground(lgray2);
                panelColor12.setBackground(lgray2);
                panelColor13.setBackground(white2);
                panelColor14.setBackground(white2);
                panelColor15.setBackground(white2);
                panelColor16.setBackground(white2);
                break;
            case 13:
                panelColor1.setBackground(blue4);
                panelColor2.setBackground(blue4);
                panelColor3.setBackground(blue4);
                panelColor4.setBackground(blue4);
                panelColor5.setBackground(blue3);
                panelColor6.setBackground(blue3);
                panelColor7.setBackground(blue3);
                panelColor8.setBackground(blue3);
                panelColor9.setBackground(blue2);
                panelColor10.setBackground(blue2);
                panelColor11.setBackground(blue2);
                panelColor12.setBackground(blue2);
                panelColor13.setBackground(blue1);
                panelColor14.setBackground(blue1);
                panelColor15.setBackground(blue1);
                panelColor16.setBackground(blue1);
                break;
            case 14:
                panelColor1.setBackground(black1);
                panelColor2.setBackground(black1);
                panelColor3.setBackground(black1);
                panelColor4.setBackground(black1);
                panelColor5.setBackground(dgray1);
                panelColor6.setBackground(dgray1);
                panelColor7.setBackground(dgray1);
                panelColor8.setBackground(dgray1);
                panelColor9.setBackground(lgray1);
                panelColor10.setBackground(lgray1);
                panelColor11.setBackground(lgray1);
                panelColor12.setBackground(lgray1);
                panelColor13.setBackground(white1);
                panelColor14.setBackground(white1);
                panelColor15.setBackground(white1);
                panelColor16.setBackground(white1);
                break;

                // -------------------------------------------------------------------------
                //  FLIPPING COLOURS 1 AND 2
                // -------------------------------------------------------------------------

            case 15:
                panelColor1.setBackground(lgray2);
                panelColor2.setBackground(white2);
                panelColor3.setBackground(dgray2);
                panelColor4.setBackground(black2);
                panelColor5.setBackground(extra01);
                panelColor6.setBackground(extra02);
                panelColor7.setBackground(extra03);
                panelColor8.setBackground(extra04);
                panelColor9.setBackground(extra05);
                panelColor10.setBackground(extra06);
                panelColor11.setBackground(extra07);
                panelColor12.setBackground(extra08);
                panelColor13.setBackground(extra09);
                panelColor14.setBackground(extra10);
                panelColor15.setBackground(extra11);
                panelColor16.setBackground(extra12);
                break;
            case 16:
                panelColor1.setBackground(blue2);
                panelColor2.setBackground(blue1);
                panelColor3.setBackground(blue3);
                panelColor4.setBackground(blue4);
                panelColor5.setBackground(extra01);
                panelColor6.setBackground(extra02);
                panelColor7.setBackground(extra03);
                panelColor8.setBackground(extra04);
                panelColor9.setBackground(extra05);
                panelColor10.setBackground(extra06);
                panelColor11.setBackground(extra07);
                panelColor12.setBackground(extra08);
                panelColor13.setBackground(extra09);
                panelColor14.setBackground(extra10);
                panelColor15.setBackground(extra11);
                panelColor16.setBackground(extra12);
                break;
            case 17:
                panelColor1.setBackground(lgray1);
                panelColor2.setBackground(white1);
                panelColor3.setBackground(dgray1);
                panelColor4.setBackground(black1);
                panelColor5.setBackground(extra01);
                panelColor6.setBackground(extra02);
                panelColor7.setBackground(extra03);
                panelColor8.setBackground(extra04);
                panelColor9.setBackground(extra05);
                panelColor10.setBackground(extra06);
                panelColor11.setBackground(extra07);
                panelColor12.setBackground(extra08);
                panelColor13.setBackground(extra09);
                panelColor14.setBackground(extra10);
                panelColor15.setBackground(extra11);
                panelColor16.setBackground(extra12);
                break;

                // FIRST LAYER
            case 18:
                panelColor1.setBackground(lgray2);
                panelColor2.setBackground(white2);
                panelColor3.setBackground(dgray2);
                panelColor4.setBackground(black2);
                panelColor5.setBackground(lgray2);
                panelColor6.setBackground(white2);
                panelColor7.setBackground(dgray2);
                panelColor8.setBackground(black2);
                panelColor9.setBackground(lgray2);
                panelColor10.setBackground(white2);
                panelColor11.setBackground(dgray2);
                panelColor12.setBackground(black2);
                panelColor13.setBackground(lgray2);
                panelColor14.setBackground(white2);
                panelColor15.setBackground(dgray2);
                panelColor16.setBackground(black2);
                break;
            case 19:
                panelColor1.setBackground(blue2);
                panelColor2.setBackground(blue1);
                panelColor3.setBackground(blue3);
                panelColor4.setBackground(blue4);
                panelColor5.setBackground(blue2);
                panelColor6.setBackground(blue1);
                panelColor7.setBackground(blue3);
                panelColor8.setBackground(blue4);
                panelColor9.setBackground(blue2);
                panelColor10.setBackground(blue1);
                panelColor11.setBackground(blue3);
                panelColor12.setBackground(blue4);
                panelColor13.setBackground(blue2);
                panelColor14.setBackground(blue1);
                panelColor15.setBackground(blue3);
                panelColor16.setBackground(blue4);
                break;
            case 20:
                panelColor1.setBackground(lgray1);
                panelColor2.setBackground(white1);
                panelColor3.setBackground(dgray1);
                panelColor4.setBackground(black1);
                panelColor5.setBackground(lgray1);
                panelColor6.setBackground(white1);
                panelColor7.setBackground(dgray1);
                panelColor8.setBackground(black1);
                panelColor9.setBackground(lgray1);
                panelColor10.setBackground(white1);
                panelColor11.setBackground(dgray1);
                panelColor12.setBackground(black1);
                panelColor13.setBackground(lgray1);
                panelColor14.setBackground(white1);
                panelColor15.setBackground(dgray1);
                panelColor16.setBackground(black1);
                break;

                // SECOND LAYER
            case 21:
                panelColor1.setBackground(lgray2);
                panelColor2.setBackground(lgray2);
                panelColor3.setBackground(lgray2);
                panelColor4.setBackground(lgray2);
                panelColor5.setBackground(white2);
                panelColor6.setBackground(white2);
                panelColor7.setBackground(white2);
                panelColor8.setBackground(white2);
                panelColor9.setBackground(dgray2);
                panelColor10.setBackground(dgray2);
                panelColor11.setBackground(dgray2);
                panelColor12.setBackground(dgray2);
                panelColor13.setBackground(black2);
                panelColor14.setBackground(black2);
                panelColor15.setBackground(black2);
                panelColor16.setBackground(black2);
                break;
            case 22:
                panelColor1.setBackground(blue2);
                panelColor2.setBackground(blue2);
                panelColor3.setBackground(blue2);
                panelColor4.setBackground(blue2);
                panelColor5.setBackground(blue1);
                panelColor6.setBackground(blue1);
                panelColor7.setBackground(blue1);
                panelColor8.setBackground(blue1);
                panelColor9.setBackground(blue3);
                panelColor10.setBackground(blue3);
                panelColor11.setBackground(blue3);
                panelColor12.setBackground(blue3);
                panelColor13.setBackground(blue4);
                panelColor14.setBackground(blue4);
                panelColor15.setBackground(blue4);
                panelColor16.setBackground(blue4);
                break;
            case 23:
                panelColor1.setBackground(lgray1);
                panelColor2.setBackground(lgray1);
                panelColor3.setBackground(lgray1);
                panelColor4.setBackground(lgray1);
                panelColor5.setBackground(white1);
                panelColor6.setBackground(white1);
                panelColor7.setBackground(white1);
                panelColor8.setBackground(white1);
                panelColor9.setBackground(dgray1);
                panelColor10.setBackground(dgray1);
                panelColor11.setBackground(dgray1);
                panelColor12.setBackground(dgray1);
                panelColor13.setBackground(black1);
                panelColor14.setBackground(black1);
                panelColor15.setBackground(black1);
                panelColor16.setBackground(black1);
                break;

                // FIRST LAYER INVERTED
            case 24:
                panelColor1.setBackground(black2);
                panelColor2.setBackground(dgray2);
                panelColor3.setBackground(white2);
                panelColor4.setBackground(lgray2);
                panelColor5.setBackground(black2);
                panelColor6.setBackground(dgray2);
                panelColor7.setBackground(white2);
                panelColor8.setBackground(lgray2);
                panelColor9.setBackground(black2);
                panelColor10.setBackground(dgray2);
                panelColor11.setBackground(white2);
                panelColor12.setBackground(lgray2);
                panelColor13.setBackground(black2);
                panelColor14.setBackground(dgray2);
                panelColor15.setBackground(white2);
                panelColor16.setBackground(lgray2);
                break;
            case 25:
                panelColor1.setBackground(blue4);
                panelColor2.setBackground(blue3);
                panelColor3.setBackground(blue1);
                panelColor4.setBackground(blue2);
                panelColor5.setBackground(blue4);
                panelColor6.setBackground(blue3);
                panelColor7.setBackground(blue1);
                panelColor8.setBackground(blue2);
                panelColor9.setBackground(blue4);
                panelColor10.setBackground(blue3);
                panelColor11.setBackground(blue1);
                panelColor12.setBackground(blue2);
                panelColor13.setBackground(blue4);
                panelColor14.setBackground(blue3);
                panelColor15.setBackground(blue1);
                panelColor16.setBackground(blue2);
                break;
            case 26:
                panelColor1.setBackground(black1);
                panelColor2.setBackground(dgray1);
                panelColor3.setBackground(white1);
                panelColor4.setBackground(lgray1);
                panelColor5.setBackground(black1);
                panelColor6.setBackground(dgray1);
                panelColor7.setBackground(white1);
                panelColor8.setBackground(lgray1);
                panelColor9.setBackground(black1);
                panelColor10.setBackground(dgray1);
                panelColor11.setBackground(white1);
                panelColor12.setBackground(lgray1);
                panelColor13.setBackground(black1);
                panelColor14.setBackground(dgray1);
                panelColor15.setBackground(white1);
                panelColor16.setBackground(lgray1);
                break;

                // SECOND LAYER INVERTED
            case 27:
                panelColor1.setBackground(black2);
                panelColor2.setBackground(black2);
                panelColor3.setBackground(black2);
                panelColor4.setBackground(black2);
                panelColor5.setBackground(dgray2);
                panelColor6.setBackground(dgray2);
                panelColor7.setBackground(dgray2);
                panelColor8.setBackground(dgray2);
                panelColor9.setBackground(white2);
                panelColor10.setBackground(white2);
                panelColor11.setBackground(white2);
                panelColor12.setBackground(white2);
                panelColor13.setBackground(lgray2);
                panelColor14.setBackground(lgray2);
                panelColor15.setBackground(lgray2);
                panelColor16.setBackground(lgray2);
                break;
            case 28:
                panelColor1.setBackground(blue4);
                panelColor2.setBackground(blue4);
                panelColor3.setBackground(blue4);
                panelColor4.setBackground(blue4);
                panelColor5.setBackground(blue3);
                panelColor6.setBackground(blue3);
                panelColor7.setBackground(blue3);
                panelColor8.setBackground(blue3);
                panelColor9.setBackground(blue1);
                panelColor10.setBackground(blue1);
                panelColor11.setBackground(blue1);
                panelColor12.setBackground(blue1);
                panelColor13.setBackground(blue2);
                panelColor14.setBackground(blue2);
                panelColor15.setBackground(blue2);
                panelColor16.setBackground(blue2);
                break;
            case 29:
                panelColor1.setBackground(black1);
                panelColor2.setBackground(black1);
                panelColor3.setBackground(black1);
                panelColor4.setBackground(black1);
                panelColor5.setBackground(dgray1);
                panelColor6.setBackground(dgray1);
                panelColor7.setBackground(dgray1);
                panelColor8.setBackground(dgray1);
                panelColor9.setBackground(white1);
                panelColor10.setBackground(white1);
                panelColor11.setBackground(white1);
                panelColor12.setBackground(white1);
                panelColor13.setBackground(lgray1);
                panelColor14.setBackground(lgray1);
                panelColor15.setBackground(lgray1);
                panelColor16.setBackground(lgray1);
                break;

        }
    }

    public void findColors(BufferedImage bi){
        int pixel = bi.getRGB(bi.getWidth() - 1, bi.getHeight() - 1);
        int R = (pixel >> 16) & 0x000000FF;
        //System.out.println("R: " + R);
        switch(R){
            case 0: // BLACK background, WHITE characters
                comboBackground.setSelectedIndex(1);
                comboTextColor.setSelectedIndex(1);
                CLUT_in_use = 0;
                break;
            case 8: // BLUE background, BLACK characters
                comboBackground.setSelectedIndex(3);
                comboTextColor.setSelectedIndex(3);
                CLUT_in_use = 1;
                break;
            case 248:   // WHITE background, BLACK characters
                comboBackground.setSelectedIndex(2);
                comboTextColor.setSelectedIndex(2);
                CLUT_in_use = 2;
                break;
            default:    // Another background, set to TRANSPARENT and GRAY
                comboBackground.setSelectedIndex(0);
                comboTextColor.setSelectedIndex(0);
                CLUT_in_use = 0;
                break;
        }

        if (checkLayers.isSelected()){
            if (checkSecondLayer.isSelected())
                CLUT_in_use += 6;
            else
                CLUT_in_use += 3;
        }
        if (checkFlip.isSelected())
            CLUT_in_use += 15;

        displayCLUT();
    }

    public void saveHalfTexture(){
        Image imgScale = imgEdit.getScaledInstance(imgEdit.getWidth(), imgEdit.getHeight()/2, Image.SCALE_SMOOTH);
        imgFinal = new BufferedImage(imgEdit.getWidth(), imgEdit.getHeight()/2, BufferedImage.TYPE_BYTE_BINARY, CLUTs[CLUT_in_use]);
        //System.out.println("Starting width: " + finalImg.getWidth());
        Graphics gr = imgFinal.createGraphics();
        //g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        gr.drawImage(imgScale, 0, 0, new Color(0,0,0), null);
        gr.dispose();

        saveEditTexture();
    }

    public void saveEditTexture(){
        String path = textfieldDestination.getText().trim();
        String filename = textfieldFilename.getText().trim();

        if (path.isEmpty()){
            path = new java.io.File(".").getAbsolutePath();
        }

        if (!path.endsWith("/"))
            path += "/";

        path += filename;
        if (!path.endsWith(".bmp"))
            path += ".bmp";

        File f = new File(path);

        try{
            ImageIO.write(imgFinal, "bmp", f);

            JOptionPane.showMessageDialog(null, path + "\nsaved succesfully.",
                    "File Saved", JOptionPane.INFORMATION_MESSAGE);
            System.out.println(path + "\nsaved succesfully.");
        }
        catch (IOException e)
        {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "An error ocurred while saving\n" + path,
                    "ERROR", JOptionPane.ERROR_MESSAGE);
        }
    }

    public void writeEdit(String text){
        // Create a new BufferedImage with the text
        BufferedImage tmp;
        //ColorModel cm = previewFile.getColorModel();
        //IndexColorModel icm = new IndexColorModel(4, 16, cm.getComponentSize(), 0, false, Transparency.OPAQUE, DataBuffer.TYPE_BYTE);
        if (previewFile.getWidth() != 0){
            tmp = new BufferedImage(previewFile.getWidth(), previewFile.getHeight(), BufferedImage.TYPE_BYTE_BINARY, CLUTs[CLUT_in_use]);
            //System.out.println("Width: " + previewFile.getWidth() + " Height: " + previewFile.getHeight());
        }
        else
            tmp = new BufferedImage(256, 256, BufferedImage.TYPE_BYTE_BINARY, CLUTs[CLUT_in_use]);
        Graphics2D g2d = tmp.createGraphics();

        // Fill the background
        switch (comboBackground.getSelectedIndex()){
            case 0: // Transparent
                //labelExplanation.setVisible(true);
                //System.out.println("No background");
                break;
            case 1: // Black
                //labelExplanation.setVisible(false);
                g2d.setPaint(new Color(0, 0, 0));
                g2d.fillRect(0, 0, tmp.getWidth(), tmp.getHeight());
                //System.out.println("Black background");
                break;
            case 2: // White
                //labelExplanation.setVisible(false);
                g2d.setPaint(new Color(248, 248, 232));
                g2d.fillRect(0, 0, tmp.getWidth(), tmp.getHeight());
                //System.out.println("White background");
                break;
            case 3: // Blue
                //labelExplanation.setVisible(false);
                g2d.setPaint(new Color(8, 200, 192));
                g2d.fillRect(0, 0, tmp.getWidth(), tmp.getHeight());
                //System.out.println("Blue background");
                break;
        }

        boolean smallFont = radioFontSmall.isSelected();

        if (!fontLoaded){
            if (smallFont)
                g2d.setFont(new Font("Sans", Font.PLAIN, 10));
            else
                g2d.setFont(new Font("Sans", Font.PLAIN, 18));
        }
        else{
            if (smallFont)
                //g2d.setFont(ac3font.deriveFont(8f));
                //g2d.setFont(new Font("Sans", Font.BOLD, 10));
                //g2d.setFont(new Font("Arial", Font.BOLD, 11));
                g2d.setFont(new Font("Segoe UI", Font.PLAIN, 10));
            else{
                //g2d.setFont(ac3font.deriveFont(18f));   // simkai
                //g2d.setFont(ac3font.deriveFont(16f));   // Antonio-Regular
                //g2d.setFont(ac3font.deriveFont(14f));   // Antonio-Bold
                g2d.setFont(ac3font.deriveFont(13f));   // Antonio-Bold-Custom
            }
        }

        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        Color colour_main = new Color(0,0,0);
        Color colour_sub = new Color(0,0,0);

        switch (comboTextColor.getSelectedIndex()){
            case 0: // Gray
                //g2d.setPaint(new Color(197, 197, 197));
                //colour_main = new Color(197, 197, 197); // almost lgray2
                colour_main = lgray2;
                colour_sub = dgray2;    // the other one might be too dark
                break;
            case 1: // White
                //g2d.setPaint(new Color(240, 240, 240));
                //colour_main = new Color(240, 240, 240); // white2
                colour_main = white2;
                colour_sub = dgray2;
                break;
            case 2: // Black
                //g2d.setPaint(new Color(56, 56, 56));
                //colour_main = new Color(56, 56, 56); // black1
                colour_main = black1;
                colour_sub = dgray1;
                break;
            case 3: // Blue-ish Black
                //g2d.setPaint(new Color(8, 56, 64));
                //colour_main = new Color(8, 56, 64); // blue1
                colour_main = blue1;
                colour_sub = blue2;
                break;
        }

        FontMetrics fm = g2d.getFontMetrics();

        // Split the text in lines
        String[] lines = text.split("\n");
        for (int i = 0; i < lines.length; i++){
            if (!fontLoaded){
                g2d.setPaint(colour_main);
                if (smallFont)
                    g2d.drawString(lines[i], 0, fm.getHeight() - 6 + (i*(fm.getHeight()-4)));
                else
                    g2d.drawString(lines[i], 0, fm.getHeight() - 8 + (i*(fm.getHeight()-4)));
            }
            else{
                if (smallFont){
                    // Draw the shadow
                    g2d.setPaint(colour_sub);
                    g2d.drawString(lines[i], 1, fm.getHeight() - 6 + (i*(fm.getHeight()-4)));
                    
                    // Draw the normal text
                    g2d.setPaint(colour_main);
                    g2d.drawString(lines[i], 0, fm.getHeight() - 6 + (i*(fm.getHeight()-4)));
                }
                else{
                    int extra_spacing = 0;
                    if (checkLineSpacing.isSelected())
                        extra_spacing = 2;
                    
                    g2d.setPaint(colour_main);
                    //g2d.drawString(lines[i], 0, fm.getHeight() - 5 + (i*(fm.getHeight()-1))); // simkai
                    //g2d.drawString(lines[i], 0, fm.getHeight() - 8 + (i*(fm.getHeight()-4)));   // Antonio-Regular
                    //g2d.drawString(lines[i], 0, fm.getHeight() - 5 + (i*(fm.getHeight()-1)));   // Antonio-Bold
                    g2d.drawString(lines[i], 0, fm.getHeight() - 2 + (i*(fm.getHeight()+ extra_spacing)));   // Antonio-Bold-Custom
                }
            }
        }
        g2d.dispose();  // Supposedly, now all we've written is in tmp

        imgEdit = tmp;

        // Send the BufferedImage to the preview
        previewEdit.writeText(imgEdit);
        previewEdit.setBounds(276, 30, imgEdit.getWidth(), imgEdit.getHeight());
        previewEdit.repaint();
    }

    public void showPreview(){
        try {
            BufferedImage img = ImageIO.read(new File(lastDirectoryFile));
            findColors(img);
            previewFile.setBounds(10, 30, img.getWidth(), img.getHeight());
            previewEdit.setBounds(276, 30, img.getWidth(), img.getHeight());
            previewFile.writeText(img);
            //icm = img.getColorModel();
            writeEdit(textareaTranslation.getText());
            //System.out.println("Original width: " + img.getWidth() + " - Edit width: " + imgEdit.getWidth());
            int newHeight = img.getHeight() + 40;
            if (newHeight > scrollPreview.getHeight()){
                panelShow.setPreferredSize(new Dimension(panelShow.getWidth(), newHeight));
                //System.out.println("Too big for the scroll.");
            }
            else{
                panelShow.setPreferredSize(new Dimension(panelShow.getWidth(), scrollPreview.getHeight()));
                //System.out.println("Fits in the scroll.");
            }
            scrollPreview.revalidate();

        } catch (IOException ex) {
            //System.out.println("Tried to open: "+ lastDirectoryFile + "/" + filename);
            Logger.getLogger(UserInterface.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton buttonDestination;
    private javax.swing.JButton buttonGenerate;
    private javax.swing.JButton buttonOriginal;
    private javax.swing.JCheckBox checkFlip;
    private javax.swing.JCheckBox checkHalf;
    private javax.swing.JCheckBox checkInverted;
    private javax.swing.JCheckBox checkLayers;
    private javax.swing.JCheckBox checkLineSpacing;
    private javax.swing.JCheckBox checkSecondLayer;
    private javax.swing.JComboBox comboBackground;
    private javax.swing.JComboBox comboTextColor;
    private javax.swing.ButtonGroup groupFontSize;
    private javax.swing.JLabel labelBackground;
    private javax.swing.JLabel labelCLUT;
    private javax.swing.JLabel labelDestination;
    private javax.swing.JLabel labelFilename;
    private javax.swing.JLabel labelOriginal;
    private javax.swing.JLabel labelOriginalPreview;
    private javax.swing.JLabel labelTextColor;
    private javax.swing.JLabel labelTranslated;
    private javax.swing.JPanel panelCLUT;
    private javax.swing.JPanel panelColor1;
    private javax.swing.JPanel panelColor10;
    private javax.swing.JPanel panelColor11;
    private javax.swing.JPanel panelColor12;
    private javax.swing.JPanel panelColor13;
    private javax.swing.JPanel panelColor14;
    private javax.swing.JPanel panelColor15;
    private javax.swing.JPanel panelColor16;
    private javax.swing.JPanel panelColor2;
    private javax.swing.JPanel panelColor3;
    private javax.swing.JPanel panelColor4;
    private javax.swing.JPanel panelColor5;
    private javax.swing.JPanel panelColor6;
    private javax.swing.JPanel panelColor7;
    private javax.swing.JPanel panelColor8;
    private javax.swing.JPanel panelColor9;
    private javax.swing.JPanel panelOriginal;
    private javax.swing.JPanel panelOutput;
    private javax.swing.JPanel panelPreview;
    private javax.swing.JPanel panelShow;
    private javax.swing.JPanel panelText;
    private javax.swing.JRadioButton radioFontBig;
    private javax.swing.JRadioButton radioFontSmall;
    private javax.swing.JScrollPane scrollPaneTexto;
    private javax.swing.JScrollPane scrollPreview;
    private javax.swing.JTextArea textareaTranslation;
    private javax.swing.JTextField textfieldDestination;
    private javax.swing.JTextField textfieldFilename;
    // End of variables declaration//GEN-END:variables

}
